"""
批量获取 ROM 的更新日志（changelog），按语种写入 logs 表的多语言分组，并回写 roms.logs。

移植自 hub.miuier.com/data/scripts/fetch_changelog.py，与本仓库原 getChangelog.py（只打印不落库）
的区别：
  * 按 ROM id 批量处理，而不是按语种逐遍扫表；
  * 多语种共用同一份请求表单（只替换 l 参数），一个 id 只查一次库；
  * 接口没有该语种译文时会回落英文，检测到与 logs_en 完全相同即跳过（需要强制写入时加 --force）；
  * 写入走 logs_store.LogStore（同一日志的多语言版本共用一行的 logs 表 + roms.logs 的 ID 引用结构）。

数据格式与 hub 的 miroms/logs_store.py 完全相同，两个项目写的是同一个库的同一张表，
因此导出的 JSON、roms.logs 的语言掩码都通用。

运行逻辑（按 ROM id 批量，而非按语种逐遍扫表）：
1. 把候选 ROM 的 logs 解回各语言，找出缺少该语种的 id 存进该语种的数组；
2. 遍历所有 id 的并集（由新到旧，id 从大到小），同一个 id 只查一次数据库拿到 ROM 信息、
   只构建一次请求表单；命中的多个语种共用这份表单，仅替换 l 参数各请求一次；
3. 每个语种处理完就把该 id 从对应数组中删除，处理下一个 id；
4. 对 cn 区域的记录同时写入 release_date，并从响应中提取卡刷包（recovery）文件名。

写入是逐条 UPDATE 且连接为 autocommit，执行即落库（不会攒到最后统一提交）；
写入失败不再被静默忽略——会计入 write_failed 并打印首个错误。

用法（脚本会把自身所在目录加入 sys.path，在任意工作目录下都能跑）：
    python3 public/MRData/scripts/fetch_changelog.py                     # 依次补全所有语种
    python3 public/MRData/scripts/fetch_changelog.py --langs ja,ko,ru    # 只处理指定语种
    python3 public/MRData/scripts/fetch_changelog.py --probe 5           # 探测接口对哪些语种真的返回了译文
    python3 public/MRData/scripts/fetch_changelog.py --dry-run --limit 5 # 只看会写什么，不落库
    python3 public/MRData/scripts/fetch_changelog.py --min-id 0 --limit 50
    python3 public/MRData/scripts/fetch_changelog.py --force --sleep 0.3

注意：--min-id 默认 46000（与 hub 一致，只补近期记录）；要补全表老记录请传 --min-id 0。
全语种全表抓取会打几千次接口，建议先用 --dry-run 估量、再按 --langs / --limit 分批补。

来源: hub.miuier.com/data/scripts/fetch_changelog.py（原 HyperOS.fans test2.py Changelog）
"""
import argparse
import json
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

import requests

import common
from database import DatabaseManager
from logs_store import (CHANGELOG_BASE_COLUMN, CHANGELOG_COLUMNS, CHANGELOG_LOCALES,
						LogStore, find_changelog_locale)

# 单个 ROM 的数据库字段（一次查询供该 id 的所有语种复用）
# logs 列为语言中性的 ID 引用结构（[[模块ID,[条目ID,...],语言掩码],...]），
# 各语言原文在 logs 表按列存放，经 LogStore.build_localized 还原为 {语言列: {...}}
ROM_INFO_SQL = (
	"SELECT device, code, region, branch, android, version, zone, logs "
	"FROM roms WHERE id = %s"
)

# 请求表单里接口真正读取的区域字段是小写 r（common.MiOTAForm 模板默认 'CN'）。
# 历史实现误写成大写 R，导致所有请求都按 CN 查询、国际/EEA 机型拿不到日志。
# 取值：CN / GL 沿用接口模板与 common 的 OTA 请求，其余区域用 roms.region 原值
# （如 mist_eea_global → eea）。若接口要求大写，只需改这张表：
REGION_FIELD_OVERRIDES = {'cn': 'CN', 'global': 'GL'}

API_URL = common.check_url
API_HEADERS = {
	'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)',
	'Connection': 'Keep-Alive',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cache-Control': 'no-cache',
	'Host': 'update.miui.com',
	'Accept-Encoding': 'gzip',
	'Cookie': 'serviceToken=;',
}


def region_field(region: str) -> str:
	"""把数据库 roms.region 映射为请求表单的 r 字段"""
	code = str(region or '').strip().lower()
	return REGION_FIELD_OVERRIDES.get(code, code)


def os_replace(ver: str) -> str:
	"""版本号 OS1 替换为 V816"""
	if 'OS1' in ver:
		return ver.replace('OS1', 'V816')
	return ver


def print_target() -> None:
	"""打印实际连接的数据库，避免「脚本跑完但看的是另一个库」"""
	try:
		print(f"数据库：{DatabaseManager.target()}"
			  f"（autocommit，逐条 UPDATE，执行即落库）")
	except Exception as exc:  # config 缺失/导入失败不应中断主流程
		print(f"（无法读取数据库配置：{type(exc).__name__}: {exc}）")


def verify_columns(locales: List[dict]) -> None:
	"""确认 logs 表已有各语言列；缺列时给出迁移指引并退出"""
	try:
		rows = DatabaseManager.execute("SHOW COLUMNS FROM logs", fetch_one=False, raise_on_error=True)
	except Exception as exc:
		print(f"✖ 无法读取 logs 表结构：{type(exc).__name__}: {exc}")
		print("  请检查 scripts/config.py 里的 host / database 是否正确、数据库是否可连")
		sys.exit(1)

	existing = {row[0] for row in rows or []}
	if 'content' not in existing:
		print("✖ logs 表仍是旧结构（缺少多语言列），请先按 db 迁移脚本补表：")
		print("  python3 public/MRData/scripts/logs_store.py   # 或执行 hub 的 migrate_logs_multilang.py")
		sys.exit(1)

	missing = [cfg['column'] for cfg in locales if cfg['column'] not in existing]
	if missing:
		print(f"✖ logs 表缺少以下语言列：{', '.join(missing)}")
		print("  新增语种需要给 logs 表 ADD COLUMN（列名与顺序见 logs_store.CHANGELOG_LOCALES）")
		sys.exit(1)


def build_changelog_form(info: dict) -> dict:
	"""构造与语种无关的请求表单；同一 ROM 的多个语种复用同一份，仅替换 l"""
	form = dict(common.MiOTAForm)

	form['d'] = info['code']
	# 接口读取的是小写 r（区域）；大写 R 是历史误加字段，不要再用
	form['r'] = region_field(info['region'])
	form['b'] = info['branch']
	form['pn'] = info['code'].split('_global')[0] if '_global' in info['code'] else info['code']
	form['c'] = info['android']
	form['sdk'] = common.sdk.get(info['android'], '36')
	form['p'] = info['device']
	# options 必须另起一份：MiOTAForm 的 options 是模板里的嵌套字典，直接改会污染后续请求
	form['options'] = dict(form.get('options', {}))
	# zone 直接取数据库 roms.zone（1=中国、2=国际），不按 region 推断
	form['options']['zone'] = info['zone']
	form['options']['cv'] = os_replace(info['version'])
	form['v'] = os_replace(info['version'])
	form['ov'] = os_replace(info['version'])

	return form


def call_api(encrypted_data: str) -> Optional[dict]:
	"""请求更新日志接口并解密应答（失败返回 None）"""
	try:
		response = requests.post(
			API_URL, headers=API_HEADERS,
			data='q=' + encrypted_data + '&s=1&t=', timeout=(5, 15),
		)
	except requests.exceptions.RequestException as exc:
		print(f"\n✖ 请求失败：{type(exc).__name__}: {exc}")
		return None

	if response.status_code != 200:
		print(f"\n✖ 接口返回 HTTP {response.status_code}")
		return None
	try:
		data = common.miui_decrypt(response.text.split('q=')[0])
	except Exception as exc:
		# 接口报错时返回的不是密文，解密会失败——把原文前 200 字打出来便于排查
		print(f"\n✖ 应答解密失败（{type(exc).__name__}: {exc}）：{response.text[:200]}")
		return None
	finally:
		response.close()
	return data if isinstance(data, dict) else None


def strip_log(data: dict) -> dict:
	"""提取日志文本内容（把 {模块: {'txt': [...]}} 压成 {模块: [...]}）"""
	result = {}
	for key, value in (data or {}).items():
		if isinstance(value, dict) and 'txt' in value:
			result[key] = value['txt']
		else:
			result[key] = value
	return result


def clean_log(d: Any) -> Any:
	"""清理日志中的特殊字符（对齐 hub 的 ChangelogManager._clean_log）

	注意：写库已改为参数化 SQL，百分号不再是必须替换的转义字符，
	但这里保持与 hub 一致，避免同一句日志在两边算出不同的 content_hash。
	"""
	if isinstance(d, dict):
		return {
			k: clean_log(v)
			for k, v in d.items()
			if v and not (isinstance(v, str) and v.isspace())
		}
	elif isinstance(d, list):
		return [
			clean_log(v)
			for v in d
			if v and not (isinstance(v, str) and v.isspace())
		]
	elif isinstance(d, str):
		return d.replace('\b', '').replace('\t', '').replace('%', '$$')\
				.replace('"', '^').replace("'", "^").replace('\n', '')
	return d


def get_changelog_for_device(info: dict, lang: str, form: Optional[dict] = None) -> Optional[dict]:
	"""获取单个设备指定语言的 changelog

	form 为 build_changelog_form() 的结果；同一 ROM 请求多个语种时传入复用即可，
	此时只替换 l 参数，其余字段完全一致。
	返回 {'changelog': 原文 JSON 字符串或 None, 'recovery': 卡刷包文件名}，请求失败返回 None。
	"""
	if form is None:
		form = build_changelog_form(info)

	payload = dict(form)
	payload['l'] = lang

	encrypted_form = common.miui_encrypt(json.dumps(payload))
	result = call_api(encrypted_form)
	if result is None:
		return None

	log = None
	recovery = None
	# 优先匹配 CurrentRom，其次 LatestRom（版本号对上才取日志）
	for key in ['CurrentRom', 'LatestRom']:
		rom = result.get(key)
		if isinstance(rom, dict) and rom.get('version') == info['version']:
			log = rom.get('changelog')
			recovery = rom.get('filename', '')
			break

	# 兜底：取 LatestRom 的 recovery（即使版本不完全匹配）
	if not recovery:
		latest = result.get('LatestRom')
		if isinstance(latest, dict):
			recovery = latest.get('filename', '')

	cleaned_log = None
	if log:
		cleaned_log = json.dumps(strip_log(clean_log(log)), ensure_ascii=False)

	return {'changelog': cleaned_log, 'recovery': recovery or ''}


def is_same_log(left: Optional[str], right: Any) -> bool:
	"""比较两条日志是否等价（用于判断接口是否回落到英文）

	left 为接口返回的原文 JSON；right 为库中现值（可能是 ID 引用结构），
	比较前统一归一化为原文对象。
	"""
	if not left or not right:
		return False
	lval = LogStore.normalize_json(left)
	rval = LogStore.normalize_json(right)
	if isinstance(lval, (dict, list)) and isinstance(rval, (dict, list)):
		return lval == rval
	return str(left).strip() == str(right).strip()


def write_rom_logs(rom_id: int, langs: dict, region: str, stats: dict, per_locale: dict,
				   dry_run: bool = False) -> bool:
	"""写入一个 ROM 的多语言日志（cn 区域同时写 release_date）

	langs 已是 {语言列: 原文对象}，由 LogStore.write_logs 重新分组写入 logs 表并返回
	roms.logs 的 ID 引用结构。写库失败会计入 write_failed 并打印首个错误，不再静默吞掉。
	"""
	prefix = "[dry-run] " if dry_run else ""
	if dry_run:
		stats['updated'] += 1
		print(f"\n{prefix}将写入 id={rom_id} 的语言：{', '.join(sorted(langs))}")
		return True

	try:
		encoded = LogStore.write_logs(langs)
	except Exception as exc:
		stats['write_failed'] += 1
		if stats['write_failed'] == 1:
			print(f"\n✖ 日志分组写入失败（id={rom_id}）：{type(exc).__name__}: {exc}")
		return False

	try:
		if region == 'cn':
			DatabaseManager.execute(
				"UPDATE roms SET logs = %s, release_date = %s WHERE id = %s",
				params=(encoded, date.today().strftime('%Y-%m-%d'), rom_id),
				raise_on_error=True,
			)
		else:
			DatabaseManager.execute(
				"UPDATE roms SET logs = %s WHERE id = %s",
				params=(encoded, rom_id), raise_on_error=True,
			)
	except Exception as exc:
		stats['write_failed'] += 1
		if stats['write_failed'] == 1:
			print(f"\n✖ 写入失败（id={rom_id}）：{type(exc).__name__}: {exc}")
		return False

	stats['updated'] += 1
	if stats['updated'] == 1:
		print(f"\n✓ 首次写入成功：id={rom_id} 语言 {', '.join(sorted(langs))}")
	return True


def select_locales(names: Optional[List[str]]) -> List[dict]:
	"""按 --langs 解析语种配置；不传则返回全部语种"""
	if not names:
		return list(CHANGELOG_LOCALES)

	selected = []
	unknown = []
	for name in names:
		item = find_changelog_locale(name)
		if item:
			selected.append(item)
		else:
			unknown.append(name)
	if unknown:
		valid = ', '.join(f"{i['column']}({i['api']})" for i in CHANGELOG_LOCALES)
		raise SystemExit(f"未知语种: {', '.join(unknown)}\n可选: {valid}")
	return selected


def collect_pending_ids(locales: List[dict], min_id: int = 0, limit: int = 0) -> Dict[str, List[int]]:
	"""每个语种查一次待补 id，返回 {列名: [待补 id...]}（由新到旧）

	更新日志是「同一日志多语言一行」的 logs 表 + roms 单列 logs 结构，
	因此不能用 `WHERE logs_ja IS NULL` 判断，改为把候选 ROM 的 logs 解回各语言，
	再挑出缺少该语言的 id。
	"""
	try:
		rows = DatabaseManager.execute(
			"SELECT id, logs FROM roms "
			"WHERE branch != 'X' AND (tag != 'CnOB' OR tag IS NULL) ORDER BY id DESC",
			fetch_one=False, raise_on_error=True,
		)
	except Exception as exc:
		print(f"✖ 查询待补记录失败：{type(exc).__name__}: {exc}")
		sys.exit(1)

	present: Dict[int, set] = {}
	for row in rows or []:
		rom_id, value = row[0], row[1]
		if not value:
			present[rom_id] = set()
			continue
		try:
			parsed = json.loads(value)
			present[rom_id] = set(LogStore.build_localized(parsed).keys())
		except (json.JSONDecodeError, TypeError):
			present[rom_id] = set()

	pending: Dict[str, List[int]] = {}
	for cfg in locales:
		column = cfg['column']
		ids = [rom_id for rom_id, langs in present.items() if column not in langs]
		raw_total = len(ids)
		if min_id:
			ids = [rom_id for rom_id in ids if rom_id > min_id]
		if limit:
			ids = ids[:limit]
		pending[column] = ids
		note = ''
		if min_id or limit:
			note = f"（共 {raw_total} 条"
			if min_id:
				note += f"，--min-id {min_id} 后 {len(ids)} 条"
			if limit:
				note += f"，--limit {limit} 截断"
			note += '）'
		print(f"{cfg['name']:<16} {cfg['api']:<6} → {column:<12} 待补 {len(ids)} 条{note}")
	return pending


def fetch_changelogs(locales: List[dict], min_id: int = 46000, limit: int = 0,
					 force: bool = False, sleep: float = 0.0, dry_run: bool = False,
					 print_form: bool = False) -> dict:
	"""按 ROM id 遍历，同一个 id 命中的多个语种只查一次库、只构建一次表单"""
	pending = collect_pending_ids(locales, min_id=min_id, limit=limit)

	# 待补集合：{列名: set(id)}，处理完一个语种就从对应集合里删掉该 id
	pending_sets = {column: set(ids) for column, ids in pending.items()}
	# reverse=True：所有语种并集后仍按 id 从大到小，主循环从最新的 ROM 开始请求
	all_ids = sorted(set().union(*pending_sets.values()), reverse=True) if pending_sets else []

	stats = {
		'total_ids': len(all_ids),
		'updated': 0, 'fallback': 0, 'empty': 0, 'failed': 0, 'missing': 0,
		'write_failed': 0, 'dry_run': dry_run,
		'print_form': print_form, '_first_form': None,
	}
	per_locale = {
		cfg['column']: {'updated': 0, 'fallback': 0, 'empty': 0, 'failed': 0, 'write_failed': 0}
		for cfg in locales
	}

	if not all_ids:
		print("没有需要处理的记录（各语种待补数组都为空）")
		stats['per_locale'] = per_locale
		return stats

	print(f"\n共 {len(all_ids)} 个 ROM 需要补日志，开始处理..."
		  f"{'（dry-run：不会写库）' if dry_run else ''}")

	# 英文列自身与中文列不需要做「回落英文」判断
	check_fallback = {
		cfg['column']: cfg['column'] not in ('logs_zh', CHANGELOG_BASE_COLUMN)
		for cfg in locales
	}

	for idx, rom_id in enumerate(all_ids, 1):
		# 命中该 id 的语种（存在时只替换 locale 重新请求）
		targets = [cfg for cfg in locales if rom_id in pending_sets[cfg['column']]]
		if not targets:
			continue

		# 每个 id 只查一次库、只构建一次表单
		info_row = DatabaseManager.query_one(ROM_INFO_SQL, params=(rom_id,))
		if not info_row:
			stats['missing'] += 1
			for cfg in targets:
				pending_sets[cfg['column']].discard(rom_id)
			continue

		info = {
			'device': info_row[0],
			'code': info_row[1],
			'region': info_row[2],
			'branch': info_row[3],
			'android': info_row[4],
			'version': info_row[5],
			'zone': info_row[6],
		}
		# 该 ROM 现有的各语言日志（语言列 -> 原文对象），新抓到的语种合并进去后整体回写
		merged: dict = {}
		if info_row[7]:
			try:
				merged = dict(LogStore.build_localized(json.loads(info_row[7])))
			except (json.JSONDecodeError, TypeError):
				merged = {}
		logs_en = merged.get(CHANGELOG_BASE_COLUMN)
		form = build_changelog_form(info)

		columns = ','.join(cfg['column'] for cfg in targets)
		if stats.get('_first_form') is None:
			stats['_first_form'] = dict(form, l=targets[0]['api'])
			print(f"首个请求：d={form['d']} pn={form['pn']} r={form['r']} zone={form['options']['zone']} "
				  f"v={form['v']} l={targets[0]['api']}")
			if stats.get('print_form'):
				print(json.dumps(stats['_first_form'], ensure_ascii=False, indent=2))
		print(f"\r{rom_id} {info['version']} {info['device']} {idx}/{len(all_ids)} [{columns}]",
			  end="", flush=True)

		fetched: dict = {}
		for cfg in targets:
			column = cfg['column']
			# 同一份表单，仅替换 l
			api_result = get_changelog_for_device(info, cfg['api'], form=form)
			pending_sets[column].discard(rom_id)

			if api_result is None:
				stats['failed'] += 1
				per_locale[column]['failed'] += 1
				if sleep:
					time.sleep(sleep)
				continue

			log = api_result.get("changelog")
			recovery = api_result.get("recovery", "")

			if log:
				if check_fallback[column] and not force and is_same_log(log, logs_en):
					# 接口没有该语种译文，返回了与英文相同的文本，跳过写入以免存一堆英文副本
					stats['fallback'] += 1
					per_locale[column]['fallback'] += 1
				else:
					try:
						fetched[column] = json.loads(log)
					except (json.JSONDecodeError, TypeError):
						fetched[column] = log
			else:
				stats['empty'] += 1
				per_locale[column]['empty'] += 1

			# 更新 recovery 卡刷包（仅当数据库中为空时）
			if recovery and not dry_run:
				try:
					DatabaseManager.execute(
						"UPDATE roms SET recovery = %s WHERE id = %s AND (recovery IS NULL OR recovery = '')",
						params=(recovery, rom_id), raise_on_error=True
					)
				except Exception as exc:
					if stats['write_failed'] == 0:
						print(f"\n✖ 更新 recovery 失败（id={rom_id}）：{type(exc).__name__}: {exc}")

			if sleep:
				time.sleep(sleep)

		if fetched:
			merged.update(fetched)
			ok = write_rom_logs(rom_id, merged, info['region'], stats, per_locale, dry_run)
			for column in fetched:
				per_locale[column]['updated' if ok else 'write_failed'] += 1

	print()
	print("\n各语种处理结果（写入 / 回落英文跳过 / 无日志 / 请求失败 / 写入失败）：")
	for cfg in locales:
		s = per_locale[cfg['column']]
		print(f"    {cfg['column']:<12} {cfg['api']:<6} {s['updated']} / {s['fallback']} / "
			  f"{s['empty']} / {s['failed']} / {s['write_failed']}")

	if stats['updated'] == 0 and not dry_run:
		print("\n⚠ 本次没有任何写入，常见原因：")
		print("   1) 接口对所有语种都返回英文原文（回落）→ 先跑 `--probe 5` 确认；确需写入加 `--force`")
		print(f"   2) 待补数组为空（如 --min-id {min_id} 过滤掉了全部记录）→ 用 `--min-id 0` 重试")
		print("   3) 写入被数据库拒绝 → 看上面的 write_failed 计数与首个报错")

	stats['per_locale'] = per_locale
	return stats


def probe(locales: List[dict], limit: int = 3, sleep: float = 0.0) -> None:
	"""探测接口对各语种的返回情况：拿最近若干条已有日志的记录逐语种比对。"""
	rows = DatabaseManager.execute(
		"SELECT id, device, code, region, branch, android, version, zone, logs FROM roms "
		"WHERE logs IS NOT NULL AND logs != '' AND branch != 'X' ORDER BY id DESC LIMIT %s",
		params=(limit,), fetch_one=False
	)
	if not rows:
		print("没有可用于探测的记录（需要已有日志的记录）")
		return

	print(f"用最近 {len(rows)} 条记录探测 {len(locales)} 个语种：\n")

	summary = {cfg['column']: {'translated': 0, 'fallback': 0, 'empty': 0, 'failed': 0}
			   for cfg in locales}

	for row in rows:
		info = {
			'device': row[1], 'code': row[2], 'region': row[3], 'branch': row[4],
			'android': row[5], 'version': row[6], 'zone': row[7],
		}
		try:
			current = LogStore.build_localized(json.loads(row[8])) if row[8] else {}
		except (json.JSONDecodeError, TypeError):
			current = {}
		logs_en = current.get(CHANGELOG_BASE_COLUMN)
		print(f"--- {info['device']} {info['version']} ({info['region']})")

		form = build_changelog_form(info)
		for cfg in locales:
			api_result = get_changelog_for_device(info, cfg['api'], form=form)
			if api_result is None:
				status = '请求失败'
				summary[cfg['column']]['failed'] += 1
			else:
				log = api_result.get('changelog')
				if not log:
					status = '接口无日志'
					summary[cfg['column']]['empty'] += 1
				elif is_same_log(log, logs_en):
					status = '与英文相同（无译文）'
					summary[cfg['column']]['fallback'] += 1
				else:
					parsed = json.loads(log)
					status = f'有独立译文：{next(iter(parsed), "")}'
					summary[cfg['column']]['translated'] += 1
			print(f"    {cfg['column']:12} {cfg['api']:6} {status}")
			if sleep:
				time.sleep(sleep)

	print('\n汇总（有译文 / 回落英文 / 接口无日志 / 失败）：')
	for cfg in locales:
		s = summary[cfg['column']]
		print(f"    {cfg['column']:12} {cfg['api']:6} {s['translated']} / {s['fallback']} / "
			  f"{s['empty']} / {s['failed']}")
	print('\n提示：若能拿到译文的语种很少，说明小米接口只提供少数语言的更新日志。')


def main() -> None:
	parser = argparse.ArgumentParser(description='获取 ROM 更新日志并写入数据库（多语种，按 ROM id 批量）')
	parser.add_argument('--langs', help='只处理指定语种，逗号分隔（可用列名 logs_ja / api locale ja_JP / 站点 locale ja / 语言名）')
	parser.add_argument('--min-id', type=int, default=46000, help='只处理 id 大于该值的记录，默认 46000；传 0 处理全表')
	parser.add_argument('--limit', type=int, default=0, help='每个语种最多收集多少条待补记录（按 id 从大到小，即最新的 N 条），0 表示不限')
	parser.add_argument('--force', action='store_true', help='接口回落英文时也写入（默认跳过，列保持 NULL）')
	parser.add_argument('--dry-run', action='store_true', help='只打印将要写入的内容，不落库')
	parser.add_argument('--print-form', action='store_true', help='打印首个请求的完整表单 JSON（核对 r / pn / zone 等字段）')
	parser.add_argument('--sleep', type=float, default=0.0, help='每次接口请求后的间隔秒数，默认 0')
	parser.add_argument('--probe', type=int, nargs='?', const=3, default=None,
						metavar='N', help='探测接口语种支持情况（默认取最近 3 条记录），不写库')
	args = parser.parse_args()

	locales = select_locales([x.strip() for x in args.langs.split(',')] if args.langs else None)

	print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始获取 changelog...")
	print_target()
	# 探测只需要英文列，方便在补列之前先确认接口支持哪些语种
	verify_columns([find_changelog_locale(CHANGELOG_BASE_COLUMN)]
				   if args.probe is not None else locales)

	if args.probe is not None:
		probe(locales, limit=args.probe, sleep=args.sleep)
		print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 探测完成")
		return

	stats = fetch_changelogs(locales, min_id=args.min_id, limit=args.limit,
							 force=args.force, sleep=args.sleep, dry_run=args.dry_run,
							 print_form=args.print_form)

	print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] changelog 获取完成："
		  f"{stats['total_ids']} 个 ROM，写入 {stats['updated']}，回落英文跳过 {stats['fallback']}，"
		  f"无日志 {stats['empty']}，请求失败 {stats['failed']}，写入失败 {stats['write_failed']}，"
		  f"记录缺失 {stats['missing']}")


if __name__ == '__main__':
	main()
