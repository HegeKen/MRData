"""
logs_store.py - 更新日志的分组存储（同一日志的多语言版本共用一行）

数据格式与 hub.miuier.com/data/scripts/miroms/logs_store.py 完全一致，两边写同一张表，
所以 **语言列顺序不能改**（roms.logs 的语言掩码按顺序取位，插队会让已入库数据的掩码错位），
新增语种只能在 CHANGELOG_LOCALES 末尾追加，并给 logs 表加同名列。

    logs
    ├─ id            自增主键（一个日志分组一个 id）
    ├─ type          module = 模块名 / log = 日志条目
    ├─ content       主内容（简体中文；无中文时取英文，再取最早出现的原文）
    ├─ content_hash  md5(content)，普通索引（同内容可因译文冲突存在多行）
    ├─ logs_zh       简体中文（与 content 同值）
    └─ logs_xx       ...其余语种各一列（列集合见 CHANGELOG_LOCALES）

roms.logs 只存 ID 引用结构：

    [[模块ID, [条目ID, ...], 语言掩码], ...]   如 [[3, [6, 8], 5], [32, [45, 48], 8]]

两个关键设计（与 hub 保持一致，否则解不回同样的日志）

1. **结构指纹聚类**：中文日志的模块 / 条目序号并不总和其他语言对应（中文可能是
   电话 / 联系人 / 短信 / 便签 四个模块，而日文、德文只返回一个「其他」模块）。
   因此只有结构指纹完全一致（模块数、每个模块条目数都相同）的语言才按序号合并成同一组；
   指纹不同的语言各自成组，作为附加模块并入总日志。

2. **语言掩码 + 冲突拆行**：logs 表按内容跨 ROM 去重，同一分组会被多个 ROM 引用。
   掩码让导出时只输出该位置在本 ROM 真正拥有的语言；若同一主内容在不同 ROM 出现互相
   冲突的译文，则另起一行保存，保证每个 ROM 的日志都能原样还原，不会「先到先得」覆盖别人。

典型用法：
    写入：encoded = LogStore.write_logs({'logs_zh': zh_obj, 'logs_en': en_obj})
          DatabaseManager.execute("UPDATE roms SET logs = %s WHERE id = %s", (encoded, rom_id))
    读取：LogStore.build_localized(json.loads(roms.logs))   # -> {'logs_zh': {...}, 'logs_en': {...}}
"""
import hashlib
import json
import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple

from database import DatabaseManager

logger = logging.getLogger(__name__)


# ==================== 语种登记表 ====================
# 顺序 = roms.logs 语言掩码的位序，只追加、不插队。
# column: logs 表列名 / api: 接口 l 参数 / site: 站点 locale / name: 语言自称
CHANGELOG_LOCALES = [
	{"column": "logs_zh", "zh": "简体中文", "api": "zh_CN", "site": "zh-Hans", "name": "简体中文", "region": "cn"},
	{"column": "logs_zh_tw", "zh": "繁体中文", "api": "zh_TW", "site": "zh-Hant", "name": "繁體中文", "region": "tw/hk/mo"},
	{"column": "logs_en", "zh": "英文", "api": "en_US", "site": "en", "name": "English", "region": "global"},
	{"column": "logs_ja", "zh": "日文", "api": "ja_JP", "site": "ja", "name": "日本語", "region": "jp"},
	{"column": "logs_ko", "zh": "韩文", "api": "ko_KR", "site": "ko", "name": "한국어", "region": "kr"},
	{"column": "logs_ru", "zh": "俄文", "api": "ru_RU", "site": "ru", "name": "Русский", "region": "ru"},
	{"column": "logs_uk", "zh": "乌克兰文", "api": "uk_UA", "site": "uk", "name": "Українська", "region": "eea"},
	{"column": "logs_pl", "zh": "波兰文", "api": "pl_PL", "site": "pl", "name": "Polski", "region": "eea"},
	{"column": "logs_de", "zh": "德文", "api": "de_DE", "site": "de", "name": "Deutsch", "region": "eea"},
	{"column": "logs_fr", "zh": "法文", "api": "fr_FR", "site": "fr", "name": "Français", "region": "eea"},
	{"column": "logs_it", "zh": "意大利文", "api": "it_IT", "site": "it", "name": "Italiano", "region": "eea"},
	{"column": "logs_es", "zh": "西班牙文", "api": "es_ES", "site": "es", "name": "Español", "region": "mx/lm/cl/gt"},
	{"column": "logs_pt", "zh": "葡萄牙文", "api": "pt_BR", "site": "pt", "name": "Português", "region": "pt/br"},
	{"column": "logs_tr", "zh": "土耳其文", "api": "tr_TR", "site": "tr", "name": "Türkçe", "region": "tr"},
	{"column": "logs_id", "zh": "印尼文", "api": "id_ID", "site": "id", "name": "Bahasa Indonesia", "region": "id"},
	{"column": "logs_vi", "zh": "越南文", "api": "vi_VN", "site": "vi", "name": "Tiếng Việt", "region": "vn"},
	{"column": "logs_th", "zh": "泰文", "api": "th_TH", "site": "th", "name": "ไทย", "region": "th"},
	# 阿拉伯语：实测接口只对 ar_EG 返回真译文，ar / ar_SA / ar_AE / ar_MA 等其余变体一律回落英文
	{"column": "logs_ar", "zh": "阿拉伯文", "api": "ar_EG", "site": "ar", "name": "العربية", "region": "eg/sa/ma"},
	# 印地语：实测只有 hi_IN 有译文
	{"column": "logs_in", "zh": "印地文", "api": "hi_IN", "site": "hi", "name": "हिन्दी", "region": "in"},
	# 维吾尔文：接口对 uy_CN / ug_CN 等变体都不返回维文译文，只能 --force 拉英文占位
	{"column": "logs_ug", "zh": "维吾尔文", "api": "ug_CN", "site": "ug", "name": "ئۇيغۇرچە", "region": "cn"},
	# 藏文：同维吾尔文，接口回落英文，需 --force
	{"column": "logs_bo", "zh": "藏文", "api": "bo_CN", "site": "bo", "name": "བོད་ཡིག", "region": "cn"},
]

# 全部语言列名（顺序即 roms.logs 语言掩码的位序）
CHANGELOG_COLUMNS = [item["column"] for item in CHANGELOG_LOCALES]

# 判断「接口没有该语种译文」的基准列：与英文完全相同即视为回落
CHANGELOG_BASE_COLUMN = "logs_en"


def find_changelog_locale(value: str) -> Dict:
	"""按列名 / api locale / 站点 locale / 语言名查找语种配置（大小写不敏感）"""
	key = str(value or "").strip().lower()
	for item in CHANGELOG_LOCALES:
		if key in (item["column"].lower(), item["api"].lower(),
				   str(item["site"]).lower(), item["name"].lower()):
			return item
	return {}


class _RowIndex:
	"""内存中的 logs 行池：按语言文本做兼容性去重，冲突则拆成新行

	- `buckets[(type, 语言列, 文本hash)]` -> 行下标列表，用于快速找到「已有该语言文本」的行；
	- 只有在**所有语言都不冲突**（该行对应语言为空或文本相同）时才复用同一行。
	"""

	__slots__ = ('rows', 'buckets', 'by_content', 'splits', 'conflicts')

	def __init__(self) -> None:
		self.rows: List[Dict[str, Any]] = []
		self.buckets: Dict[Tuple[str, str, str], List[int]] = {}
		self.by_content: Dict[Tuple[str, str], List[int]] = {}
		self.splits = 0
		self.conflicts: List[Tuple[str, str, str, str, str]] = []

	def seed(self, rows: List[Dict[str, Any]]) -> None:
		"""把数据库中已有的行灌进行池（保留 id），使写入侧与导出侧共用同一套匹配逻辑"""
		for row in rows:
			self.rows.append({
				'id': int(row['id']),
				'type': row['type'],
				'content': row['content'],
				'texts': dict(row['texts']),
				'dirty': False,
			})
			self._register(len(self.rows) - 1)

	def flush(self) -> None:
		"""把行池的变更落库：新行 INSERT（逐条取 lastrowid），补齐语言的行 UPDATE（COALESCE）

		落库前会校验行池里已有的 id 是否仍然存在：长时间运行的进程（如定时抓取）可能持有
		已被其它进程合并 / 删除的行，若不校验就会往 roms.logs 写死引用。失效的行会针对
		最新数据重新解析（复用幸存的分组，或改为新插入一行）。
		"""
		existing_ids = [int(row['id']) for row in self.rows if row.get('id') is not None]
		stale = LogStore._missing_ids(existing_ids)
		if stale:
			fresh = LogStore.load_index(force=True)
			for row in self.rows:
				if row.get('id') is None or int(row['id']) not in stale:
					continue
				found = fresh.resolve(row['type'], row['texts'])
				if found is not None and fresh.rows[found].get('id') is not None:
					row['id'] = int(fresh.rows[found]['id'])
				else:
					row['id'] = None   # 没有可复用的分组，按新行插入
				row['dirty'] = False
			logger.warning("行池中有 %d 个分组已被其它进程删除，已重新解析", len(stale))

		fills: List[Tuple[int, Dict[str, str]]] = []
		for row in self.rows:
			if row.get('id') is None:
				row['id'] = LogStore._insert_row(row)
				row['dirty'] = False
			elif row.get('dirty'):
				fills.append((int(row['id']), row['texts']))
				row['dirty'] = False
		for group_id, texts in fills:
			LogStore._fill_row(group_id, texts)
		if fills or any(r.get('id') for r in self.rows):
			LogStore._groups = None

	def _register(self, index: int) -> None:
		row = self.rows[index]
		for column, value in row['texts'].items():
			key = (row['type'], column, LogStore._hash(value))
			bucket = self.buckets.setdefault(key, [])
			if index not in bucket:
				bucket.append(index)
		key = (row['type'], LogStore._hash(row['content']))
		bucket = self.by_content.setdefault(key, [])
		if index not in bucket:
			bucket.append(index)

	def _candidates(self, log_type: str, texts: Dict[str, str]) -> List[int]:
		"""按主内容 hash + 各语言文本 hash 收集候选行下标"""
		candidates: List[int] = []
		seen = set()
		for index in self.by_content.get((log_type, LogStore._hash(LogStore._primary(texts))), ()):
			seen.add(index)
			candidates.append(index)
		for column, value in texts.items():
			for index in self.buckets.get((log_type, column, LogStore._hash(value)), ()):
				if index not in seen:
					seen.add(index)
					candidates.append(index)
		return candidates

	def lookup(self, log_type: str, texts: Dict[str, str]) -> Optional[int]:
		"""只读查找：返回**已包含**这些语言文本的行下标（不复用、不新建）

		用于「行池已建好后」的第二遍遍历（如批量迁移回写 roms.logs），
		保证写出的 id 一定落在已入库的行上。
		"""
		texts = {column: LogStore.normalize(value) for column, value in (texts or {}).items()
				 if column in LogStore.LANG_COLUMNS and LogStore.normalize(value)}
		if not texts:
			return None
		for index in self._candidates(log_type, texts):
			row = self.rows[index]
			if all(row['texts'].get(column) == value for column, value in texts.items()):
				return index
		return None

	def resolve(self, log_type: str, texts: Dict[str, str]) -> Optional[int]:
		"""找到可复用的行（缺的语言补上、已有的语言必须一致），没有则新建一行"""
		texts = {column: LogStore.normalize(value) for column, value in (texts or {}).items()
				 if column in LogStore.LANG_COLUMNS and LogStore.normalize(value)}
		if not texts:
			return None

		candidates = self._candidates(log_type, texts)
		for index in candidates:
			row = self.rows[index]
			if all(row['texts'].get(column) in (None, value) for column, value in texts.items()):
				for column, value in texts.items():
					if not row['texts'].get(column):
						row['texts'][column] = value
						row['dirty'] = True
				# 补上中文后主内容以中文为准（保证 content 始终是中文优先）
				zh_text = row['texts'].get(LogStore.ZH_COLUMN)
				if zh_text and row['content'] != zh_text:
					row['content'] = zh_text
					row['dirty'] = True
				self._register(index)
				return index

		if candidates:
			# 主内容相同但译文冲突：另起一行（保证两个 ROM 的日志都能原样还原）
			self.splits += 1
		row = {'id': None, 'type': log_type, 'content': LogStore._primary(texts),
			   'texts': dict(texts), 'dirty': False}
		self.rows.append(row)
		index = len(self.rows) - 1
		self._register(index)
		return index


class LogStore:
	"""logs 表的读写入口（写入去重 + 还原多语言日志）"""

	TYPE_MODULE = 'module'
	TYPE_LOG = 'log'

	# 语言列（logs_zh 在最前，其余顺序与 CHANGELOG_LOCALES 一致）
	LANG_COLUMNS: Tuple[str, ...] = tuple(CHANGELOG_COLUMNS)
	LANG_INDEX: Dict[str, int] = {column: i for i, column in enumerate(LANG_COLUMNS)}
	ZH_COLUMN = 'logs_zh'
	EN_COLUMN = 'logs_en'

	_LANG_COMMENTS: Dict[str, str] = {
		item['column']: f"{item['zh']}（{item['api']}）" for item in CHANGELOG_LOCALES
	}

	_table_ensured = False
	# 整表行池：写入侧用它做「语言不冲突即可复用」的匹配
	_index: Optional['_RowIndex'] = None
	# id -> {'type', 'texts'}，导出侧缓存
	_groups: Optional[Dict[int, Dict[str, Any]]] = None
	# 最近一次写入的冲突拆行统计
	last_conflicts: List[Tuple[str, str, str, str, str]] = []

	# ==================== 基础 ====================

	@classmethod
	def create_sql(cls, table: str = 'logs') -> str:
		"""生成 logs 建表语句（列随 CHANGELOG_LOCALES 自动增减）"""
		langs = "\n".join(
			f"  `{column}` longtext COLLATE utf8mb4_bin COMMENT '{cls._LANG_COMMENTS[column]}',"
			for column in cls.LANG_COLUMNS
		)
		return (
			f"CREATE TABLE IF NOT EXISTS `{table}` (\n"
			f"  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键（同一日志的各语言版本共用一行）',\n"
			f"  `type` varchar(8) COLLATE utf8mb4_bin NOT NULL COMMENT '日志类型：module=模块名 / log=日志条目',\n"
			f"  `content` text COLLATE utf8mb4_bin NOT NULL COMMENT '主内容（简体中文；无中文时取英文，再取最早出现的原文）',\n"
			f"  `content_hash` char(32) COLLATE utf8mb4_bin NOT NULL COMMENT 'content 的 MD5（hex），查专用索引（同内容可因译文冲突存在多行）',\n"
			f"{langs}\n"
			f"  PRIMARY KEY (`id`),\n"
			f"  KEY `idx_type_hash` (`type`, `content_hash`)\n"
			f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin"
		)

	@classmethod
	def ensure_table(cls) -> None:
		"""确保 logs 表存在（已存在时是空操作，列集合与 hub 的迁移脚本一致）"""
		if cls._table_ensured:
			return
		DatabaseManager.execute(cls.create_sql(), raise_on_error=True)
		cls._table_ensured = True

	@staticmethod
	def normalize(content: Any) -> str:
		"""主内容归一化：去掉首尾空白（接口原文常带前导空格与尾随空格，归一化后才能正确去重）"""
		return str(content if content is not None else '').strip()

	@staticmethod
	def _hash(content: str) -> str:
		return hashlib.md5(content.encode('utf-8')).hexdigest()

	@classmethod
	def signature(cls, log_type: str, content: str, texts: Dict[str, str]) -> str:
		"""一行日志的完整签名（类型 + 主内容 + 各语言文本），用于精确匹配已有行"""
		parts = [log_type, content]
		for column in cls.LANG_COLUMNS:
			value = texts.get(column) or ''
			if value:
				parts.append(f'{column}={value}')
		return hashlib.md5('\x1f'.join(parts).encode('utf-8')).hexdigest()

	@staticmethod
	def is_encoded(parsed: Any) -> bool:
		"""判断解析后的值是否为 ID 引用结构 [[mid, [lids...], mask?], ...]"""
		if not isinstance(parsed, list):
			return False
		for item in parsed:
			if not (isinstance(item, list) and len(item) in (2, 3)
					and isinstance(item[0], int) and isinstance(item[1], list)):
				return False
			if len(item) == 3 and not isinstance(item[2], int):
				return False
		return True

	@staticmethod
	def mask_of(columns: Sequence[str]) -> int:
		"""语言列集合 -> 语言掩码"""
		mask = 0
		for column in columns:
			mask |= 1 << LogStore.LANG_INDEX[column]
		return mask

	@classmethod
	def columns_of(cls, mask: int) -> List[str]:
		"""语言掩码 -> 语言列列表（按 LANG_COLUMNS 顺序）"""
		return [column for i, column in enumerate(cls.LANG_COLUMNS) if (mask >> i) & 1]

	# ==================== 写入侧 ====================

	@staticmethod
	def _primary(texts: Dict[str, str]) -> str:
		"""一个分组的「主内容」：优先简体中文，其次英文，最后任一语言"""
		for column in (LogStore.ZH_COLUMN, LogStore.EN_COLUMN):
			value = LogStore.normalize(texts.get(column))
			if value:
				return value
		for value in texts.values():
			value = LogStore.normalize(value)
			if value:
				return value
		return ''

	@classmethod
	def _items(cls, obj: Any) -> List[Tuple[str, List[str]]]:
		"""把一个语言结构规整为 [(模块, [条目, ...]), ...]（去掉空模块）"""
		items: List[Tuple[str, List[str]]] = []
		for module, lines in (obj or {}).items():
			if not str(module or '').strip():
				continue
			if not isinstance(lines, list):
				lines = [lines]
			items.append((str(module).strip(), [str(x) for x in lines]))
		return items

	@classmethod
	def shape(cls, obj: Any) -> Tuple[int, ...]:
		"""结构指纹：(模块数, 各模块条目数...)，用于判断两门语言能否按序号对齐"""
		items = cls._items(obj)
		return tuple([len(items)] + [len(lines) for _, lines in items])

	@classmethod
	def cluster_languages(cls, langs: Dict[str, Any]) -> List[List[str]]:
		"""把各语言按结构指纹聚类；只有指纹完全相同的语言才允许按序号对齐

		返回的簇按「含简体中文 → 含英文 → 语言数降序」排序，
		保证总日志以中文结构为主、其余结构作为附加模块追加在后。
		"""
		groups: Dict[Tuple[int, ...], List[str]] = {}
		for column in cls.LANG_COLUMNS:
			obj = (langs or {}).get(column)
			if not obj:
				continue
			groups.setdefault(cls.shape(obj), []).append(column)

		def rank(item: Tuple[Tuple[int, ...], List[str]]) -> Tuple[int, int]:
			_, cols = item
			if cls.ZH_COLUMN in cols:
				priority = 0
			elif cls.EN_COLUMN in cols:
				priority = 1
			else:
				priority = 2
			return (priority, -len(cols))

		clusters = [cols for _, cols in sorted(groups.items(), key=rank)]
		for cols in clusters:
			cols.sort(key=lambda c: cls.LANG_INDEX[c])
		return clusters

	@classmethod
	def compose(cls, langs: Dict[str, Any]) -> List[Dict[str, Any]]:
		"""把多语言结构按「结构指纹聚类 → 簇内按序号对齐」组合成一组分组位置

		返回 [{'texts': {列名: 模块文本}, 'entries': [{'texts': {列名: 条目文本}}, ...],
		       'mask': 语言掩码}, ...]
		"""
		positions: List[Dict[str, Any]] = []
		for columns in cls.cluster_languages(langs or {}):
			items = {column: cls._items(langs[column]) for column in columns}
			canonical = columns[0]
			mask = cls.mask_of(columns)
			for index, (_, lines) in enumerate(items[canonical]):
				texts: Dict[str, str] = {}
				for column in columns:
					module = items[column][index][0].strip()
					if module:
						texts[column] = module
				entries: List[Dict[str, Any]] = []
				for j in range(len(lines)):
					item: Dict[str, str] = {}
					for column in columns:
						line = items[column][index][1][j]
						if str(line).strip():
							item[column] = str(line).strip()
					entries.append({'texts': item})
				positions.append({'texts': texts, 'entries': entries, 'mask': mask})
		return positions

	@classmethod
	def new_index(cls) -> '_RowIndex':
		"""新建一个可跨多次调用共享的内存行池（批量迁移用）"""
		return _RowIndex()

	@classmethod
	def build_rows(cls, positions: List[Dict[str, Any]],
				   index: Optional['_RowIndex'] = None,
				   mutate: bool = True) -> Tuple[List[Dict[str, Any]], List[List[Any]]]:
		"""把分组位置解析成行池与引用关系

		传入 index 可在多次调用间共享行池（如批量迁移时跨 ROM 去重）。
		mutate=False 时只做只读查找（不再补全 / 新建行），用于行池建好后的第二遍遍历。
		返回 (rows, refs)：rows 为待写入行列表；refs 为
		[(模块行下标, [条目行下标, ...], 语言掩码), ...]。
		"""
		index = index if index is not None else _RowIndex()
		resolver = index.resolve if mutate else index.lookup
		refs: List[List[Any]] = []
		for position in positions:
			module_index = resolver(cls.TYPE_MODULE, position['texts'])
			if module_index is None:
				if mutate:
					continue
				raise RuntimeError(f"行池中找不到模块分组: {position['texts']}")
			entry_indices = []
			for entry in position['entries']:
				entry_index = resolver(cls.TYPE_LOG, entry['texts'])
				if entry_index is not None:
					entry_indices.append(entry_index)
			refs.append([module_index, entry_indices, int(position.get('mask', 0))])
		cls.last_conflicts = index.conflicts
		return index.rows, refs

	@classmethod
	def _missing_ids(cls, ids: Sequence[int]) -> set:
		"""返回给定 id 中已不存在的部分（分批查库）"""
		wanted = {int(i) for i in ids}
		if not wanted:
			return set()
		found = set()
		chunk_list = list(wanted)
		for i in range(0, len(chunk_list), 500):
			chunk = chunk_list[i:i + 500]
			rows = DatabaseManager.query_all(
				f"SELECT `id` FROM `logs` WHERE `id` IN ({','.join(['%s'] * len(chunk))})",
				params=tuple(chunk))
			found.update(int(row[0]) for row in rows or [])
		return wanted - found

	@classmethod
	def _fetch_all_rows(cls) -> List[Dict[str, Any]]:
		"""整表载入（id / type / content / texts），作为写入侧的行池来源"""
		columns = ', '.join(f'`{c}`' for c in cls.LANG_COLUMNS)
		rows = DatabaseManager.query_all(
			f"SELECT `id`, `type`, `content`, {columns} FROM `logs`")
		found: List[Dict[str, Any]] = []
		for row in rows or []:
			texts = {column: row[3 + i] for i, column in enumerate(cls.LANG_COLUMNS) if row[3 + i]}
			found.append({'id': int(row[0]), 'type': row[1], 'content': row[2], 'texts': texts})
		return found

	@classmethod
	def load_index(cls, force: bool = False) -> '_RowIndex':
		"""载入（并缓存）整表行池，供写入侧做「语言不冲突即可复用」的匹配

		只按 content_hash 找候选会让「同一日志、不同主内容」的行永远匹配不上
		（例如 content=相册 与 content=Gallery 其实是同一模块），
		因此写入侧在整表行池里按语言文本做兼容匹配，与导出逻辑完全一致。
		"""
		if cls._index is None or force:
			cls.ensure_table()
			index = _RowIndex()
			index.seed(cls._fetch_all_rows())
			cls._index = index
			logger.info("logs 行池已载入: %d 条", len(index.rows))
		return cls._index

	@classmethod
	def _insert_row(cls, row: Dict[str, Any]) -> int:
		"""插入一行并返回自增 id（逐条插入以拿到 lastrowid）"""
		columns = ['`type`', '`content`', '`content_hash`'] + [f'`{c}`' for c in cls.LANG_COLUMNS]
		params: List[Any] = [row['type'], row['content'], cls._hash(row['content'])]
		params.extend([row['texts'].get(c) or None for c in cls.LANG_COLUMNS])
		new_id = DatabaseManager.insert(
			f"INSERT INTO `logs` ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})",
			params=tuple(params), raise_on_error=True,
		)
		if new_id:
			return new_id
		# 兜底：驱动没给出 lastrowid 时按内容反查刚插入的行
		found = DatabaseManager.query_one(
			"SELECT `id` FROM `logs` WHERE `type` = %s AND `content_hash` = %s "
			"AND `content` = %s ORDER BY `id` DESC LIMIT 1",
			params=(row['type'], cls._hash(row['content']), row['content']),
		)
		if not found:
			raise RuntimeError(f"logs 表写入后未查到记录: type={row['type']} content={row['content'][:40]!r}")
		return int(found[0])

	@classmethod
	def _fill_row(cls, group_id: int, texts: Dict[str, str]) -> None:
		"""给已有行补齐缺失的语言列（COALESCE，不覆盖已有译文）"""
		sets = [c for c in cls.LANG_COLUMNS if texts.get(c)]
		if not sets:
			return
		DatabaseManager.execute(
			"UPDATE `logs` SET " + ', '.join(f'`{c}` = COALESCE(`{c}`, %s)' for c in sets)
			+ " WHERE `id` = %s",
			params=tuple([texts[c] for c in sets] + [group_id]), raise_on_error=True,
		)

	@classmethod
	def ensure_ids(cls, rows: List[Dict[str, Any]]) -> List[int]:
		"""把一批内存行落库并返回与 rows 等长的 id 列表

		匹配规则与 load_index 一致：类型相同且各语言不冲突即视为同一行。
		"""
		if not rows:
			return []
		index = cls.load_index()
		result: List[Optional[int]] = []
		for row in rows:
			row['sig'] = cls.signature(row['type'], row['content'], row['texts'])
			found = index.resolve(row['type'], row['texts'])
			if found is None:
				raise RuntimeError(f"logs 行解析失败: {row['content'][:40]!r}")
			index.rows[found]['content'] = row['content']
			result.append(found)
		index.flush()
		return [int(index.rows[i]['id']) for i in result]

	@classmethod
	def encode_refs(cls, refs: List[List[Any]], ids: Sequence[int]) -> str:
		"""refs（行下标引用）+ id 列表 -> roms.logs 的值：[[模块ID,[条目ID,...],掩码],...]"""
		pairs: List[List[Any]] = []
		for module_index, entry_indices, mask in refs:
			pairs.append([ids[module_index], [ids[i] for i in entry_indices], int(mask)])
		return json.dumps(pairs, ensure_ascii=False)

	@classmethod
	def write_logs(cls, langs: Dict[str, Any], dry_run: bool = False,
				   expand_mask: bool = False) -> str:
		"""写入一个 ROM 的多语言日志，返回 roms.logs 的值（ID 引用结构 JSON 字符串）

		langs = {语言列: 该语言结构}，结构指纹一致的语言会自动合并为一组；
		写入前会把整张 logs 表载入内存行池，按「类型相同 + 各语言不冲突」匹配已有分组
		（同一日志即便主内容不同也能认出来），只补齐缺失语言，不覆盖已有译文。

		expand_mask=True 时语言掩码取「模块分组与全部条目的公共语言」，
		这样复用了库里已有多语言分组时，能顺带拿到中英文之外的其他译文。
		"""
		positions = cls.compose(langs or {})
		index = cls.load_index()
		_, refs = cls.build_rows(positions, index)
		if dry_run:
			ids = [r['id'] if r.get('id') is not None else i + 1 for i, r in enumerate(index.rows)]
			return cls._encode_refs(refs, ids, expand_mask, index.rows)

		index.flush()
		ids = [int(r['id']) for r in index.rows]
		return cls._encode_refs(refs, ids, expand_mask, index.rows)

	@classmethod
	def _encode_refs(cls, refs: List[List[Any]], ids: List[int], expand_mask: bool,
					 rows: List[Dict[str, Any]]) -> str:
		if not expand_mask:
			return cls.encode_refs(refs, ids)
		pairs: List[List[Any]] = []
		for module_index, entry_indices, mask in refs:
			common = set(rows[module_index]['texts'])
			for entry_index in entry_indices:
				common &= set(rows[entry_index]['texts'])
			new_mask = cls.mask_of([c for c in cls.LANG_COLUMNS if c in common])
			pairs.append([ids[module_index], [ids[i] for i in entry_indices], new_mask or mask])
		return json.dumps(pairs, ensure_ascii=False)

	@classmethod
	def encode_value(cls, value: Any, canonical_column: str = ZH_COLUMN) -> Any:
		"""待写入列的值：原文 JSON -> ID 结构 JSON；已是 ID 结构则原样返回（幂等）

		canonical_column 指定原文 JSON 属于哪门语言（默认简体中文）。
		"""
		if not value:
			return value
		try:
			parsed = json.loads(value) if isinstance(value, str) else value
		except (json.JSONDecodeError, TypeError):
			return value
		if cls.is_encoded(parsed):
			return value
		if isinstance(parsed, dict):
			return cls.write_logs({canonical_column: parsed})
		return value

	# ==================== 读取 / 还原侧 ====================

	@classmethod
	def load_groups(cls, force: bool = False) -> Dict[int, Dict[str, Any]]:
		"""全量载入 logs 表（id -> {'type', 'texts'}），还原时纯内存映射"""
		if cls._groups is not None and not force:
			return cls._groups
		cls.ensure_table()
		columns = ', '.join(f'`{c}`' for c in cls.LANG_COLUMNS)
		rows = DatabaseManager.query_all(f"SELECT `id`, `type`, `content`, {columns} FROM `logs`")
		groups: Dict[int, Dict[str, Any]] = {}
		for row in rows or []:
			texts = {column: row[3 + i] for i, column in enumerate(cls.LANG_COLUMNS) if row[3 + i]}
			if not texts.get(cls.ZH_COLUMN) and row[2]:
				texts[cls.ZH_COLUMN] = row[2]
			groups[int(row[0])] = {'type': row[1], 'texts': texts}
		cls._groups = groups
		logger.info("logs 表已载入内存: %d 条", len(groups))
		return groups

	@classmethod
	def decode_structure(cls, pairs: Any) -> List[Tuple[Dict[str, Any], List[Dict[str, Any]], int]]:
		"""ID 引用结构 -> [(模块分组, [条目分组, ...], 语言掩码), ...]（缺失 id 跳过）"""
		if not isinstance(pairs, list):
			return []
		groups = cls.load_groups()
		result = []
		for item in pairs:
			if not (isinstance(item, list) and len(item) in (2, 3)):
				continue
			module = groups.get(int(item[0]))
			if module is None:
				continue
			entries = [groups[int(lid)] for lid in item[1]
					   if isinstance(lid, int) and int(lid) in groups]
			if len(item) == 3 and isinstance(item[2], int):
				mask = int(item[2])
			else:
				mask = cls.mask_of([c for c in cls.LANG_COLUMNS if module['texts'].get(c)])
			result.append((module, entries, mask))
		return result

	@classmethod
	def _entry_text(cls, group: Dict[str, Any], column: str) -> Optional[str]:
		"""条目文本：该语言缺失时回落英文、再回落中文；简体中文自身不回落"""
		text = group['texts'].get(column)
		if text:
			return text
		if column == cls.ZH_COLUMN:
			return None
		return group['texts'].get(cls.EN_COLUMN) or group['texts'].get(cls.ZH_COLUMN) or None

	@classmethod
	def build_localized(cls, pairs: Any) -> Dict[str, Dict[str, Any]]:
		"""ID 引用结构 -> {语言列: {模块: [条目, ...]}}（导出格式）

		只输出语言掩码里包含的语言，避免跨 ROM 复用分组时把别的语言带出来。
		"""
		result: Dict[str, Dict[str, Any]] = {}
		for module, entries, mask in cls.decode_structure(pairs):
			for index, column in enumerate(cls.LANG_COLUMNS):
				if not (mask >> index) & 1:
					continue
				module_text = module['texts'].get(column)
				if not module_text:
					continue
				lines = []
				for entry in entries:
					text = cls._entry_text(entry, column)
					if text:
						lines.append(text)
				# 空条目的模块也保留（上游日志里确实存在 {"基础体验": []} 这类空模块）
				result.setdefault(column, {}).setdefault(module_text, []).extend(lines)
		# 语言键按 LANG_COLUMNS 顺序输出，保证导出文件稳定、diff 友好
		return {column: result[column] for column in cls.LANG_COLUMNS if column in result}

	@classmethod
	def localized_value(cls, pairs: Any, column: str) -> Optional[Dict[str, Any]]:
		"""只要某一门语言的日志（缺失返回 None）"""
		return cls.build_localized(pairs).get(column)

	@classmethod
	def decode(cls, pairs: Any) -> Dict[str, Any]:
		"""ID 引用结构 -> 简体中文原文对象"""
		return cls.build_localized(pairs).get(cls.ZH_COLUMN) or {}

	@classmethod
	def decode_value(cls, parsed: Any) -> Any:
		"""解析后的列值：ID 结构 -> 多语言对象；其余（旧格式/异常值）原样返回"""
		if cls.is_encoded(parsed):
			return cls.build_localized(parsed)
		return parsed

	@classmethod
	def normalize_json(cls, value: Any) -> Any:
		"""比较用归一化：ID 结构解码为多语言对象，其余原样返回解析结果"""
		if not value or not isinstance(value, str):
			return value
		try:
			parsed = json.loads(value)
		except (json.JSONDecodeError, TypeError):
			return value
		return cls.decode_value(parsed)

	# ==================== 维护 ====================

	@classmethod
	def refresh_cache(cls) -> None:
		"""全量刷新缓存（读取侧行池 + 写入侧行池）"""
		cls._groups = None
		cls._index = None

	@classmethod
	def count(cls) -> int:
		"""logs 表行数"""
		row = DatabaseManager.query_one("SELECT COUNT(*) FROM `logs`")
		return int(row[0]) if row else 0

	@classmethod
	def prune_unused(cls) -> int:
		"""删除没有被任何 roms.logs / dev.logs 引用的日志行（返回删除行数）"""
		used = set()
		for table in ('roms', 'dev'):
			last_id = 0
			while True:
				rows = DatabaseManager.query_all(
					f"SELECT `id`, `logs` FROM `{table}` WHERE `id` > %s AND `logs` IS NOT NULL "
					f"ORDER BY `id` LIMIT 500", params=(last_id,))
				if not rows:
					break
				last_id = rows[-1][0]
				for _, value in rows:
					try:
						parsed = json.loads(value)
					except (json.JSONDecodeError, TypeError):
						continue
					if not isinstance(parsed, list):
						continue
					for item in parsed:
						if isinstance(item, list) and len(item) >= 2:
							used.add(int(item[0]))
							for entry_id in item[1]:
								used.add(int(entry_id))
		all_ids = [int(row[0]) for row in DatabaseManager.query_all("SELECT `id` FROM `logs`") or []]
		dead = [group_id for group_id in all_ids if group_id not in used]
		for i in range(0, len(dead), 500):
			chunk = dead[i:i + 500]
			DatabaseManager.execute(
				f"DELETE FROM `logs` WHERE `id` IN ({','.join(['%s'] * len(chunk))})",
				params=tuple(chunk), raise_on_error=True)
		if dead:
			cls.refresh_cache()
		return len(dead)


if __name__ == '__main__':
	# 建表 / 巡检：logs 表已存在时是空操作，缺列（新增语种后）需要手工 ADD COLUMN
	import sys

	print(f"数据库：{DatabaseManager.target()}")
	LogStore.ensure_table()
	rows = DatabaseManager.query_all("SHOW COLUMNS FROM logs")
	existing = [row[0] for row in rows or []]
	missing = [c for c in CHANGELOG_COLUMNS if c not in existing]
	print(f"logs 表语言列：{len(existing) - 4} / {len(CHANGELOG_COLUMNS)}")
	if missing:
		print(f"✖ 缺少语言列（需要 ADD COLUMN）：{', '.join(missing)}")
		sys.exit(1)
	print(f"logs 表行数：{LogStore.count()}")
