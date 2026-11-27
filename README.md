# MRData
## 项目详情| Repository Info

此项目是新版 [MIUI官方ROM仓库](https://roms.miuier.com) ，即 [NuxtMR](https://github.com/HegeKen/NuxtMR)  所使用到的各项组件以及数据的仓库

This repository contains main assets and data used in [NuxtMR](https://github.com/HegeKen/NuxtMR) project， the new version of [MIUIROMS](https://roms.miuier.com) .

> **⚠️ 数据已迁移 | Data has been migrated**
>
> `data/` 下的 JSON 数据已迁移至 [miroms](https://github.com/HegeKen/miroms) 数据仓库：数据统一存放在 MySQL，由 `scripts/exporter.py` 导出为 `api/v1`（以及 `v2` / `v3`）接口，站点通过 `https://api.miuier.com/api/v1` 读取。[NuxtMR](https://github.com/HegeKen/NuxtMR) 现已直接请求该 API（见 `app/config/api.ts` 的 `BASE_URL`），不再读取本仓库的 `data/`。
>
> 本仓库的 `data/` 仅作为迁移来源与历史对照保留，**请勿再手动修改**；路径对照与已知差异见下方「迁移说明 | Migration Notice」。
>
> All JSON data under `data/` has been migrated to the [miroms](https://github.com/HegeKen/miroms) repository. It is stored in MySQL, exported to `api/v1` (plus `v2` / `v3`) by `scripts/exporter.py`, and served from `https://api.miuier.com/api/v1`. [NuxtMR](https://github.com/HegeKen/NuxtMR) now requests that API directly (see `BASE_URL` in `app/config/api.ts`) instead of reading `data/` here.
>
> `data/` is kept only as the migration source and historical reference — **do not edit it by hand**. See "Migration Notice" below for the path mapping and known differences.

### 文件夹详情 | Folder Info

### `assets`

此文件夹是  [NuxtMR](https://github.com/HegeKen/NuxtMR)  所使用到的[MDUI](https://github.com/zdhxiong/mdui)代码以及部分JS库源码。如此分割后，变更CSS和JS部分代码后，无须再次生成网站，即可生效。

This folder contains [MDUI](https://github.com/zdhxiong/mdui) components used in [NuxtMR](https://github.com/HegeKen/NuxtMR) , and other JS libraries . With this seperation, when changes made to the CSS & JS Part , no need for a re-generation of the website.

> 现状：属于旧版静态站点时代的产物，现行 Nuxt 源码已不再引用，保留供旧页面与外部链接继续访问。
> Status: legacy from the static-site era; no longer referenced by the current Nuxt source, kept for old pages and external links.

### `data`

此文件夹是 [NuxtMR](https://github.com/HegeKen/NuxtMR)  所使用到的数据源 ， 全部用JSON文件格式的形式保存。

This folder source data to form [NuxtMR](https://github.com/HegeKen/NuxtMR) , all data is stored in JSON data format.

> **已迁移**：不再是站点数据源，迁往 [miroms](https://github.com/HegeKen/miroms) 仓库的 `api/v1/`，详见「迁移说明」。
> **Migrated**: no longer the site data source; moved to `api/v1/` in the [miroms](https://github.com/HegeKen/miroms) repository — see "Migration Notice".

### `script`

该文件夹为老的爬虫文件，该文件夹里包含我自己尝试成功或失败的Python爬虫脚本，9月末已实现卡刷包抓取，新爬虫脚本在`scripts`文件夹中。

This folder contains old Python codes I used, and I managed to crawl recovery roms late september, new scripts are in `scripts` folder.

### `scripts`

该文件夹里包含我目前在用的爬虫脚本，现可以抓取卡刷包、线刷包。

This folder contains Python codes I'm currently using to get recovery and fastboot roms.

> 现状：抓取 / 导出脚本已统一收敛到 [miroms](https://github.com/HegeKen/miroms) 仓库的 `scripts/`（与本仓库脚本共用同一个 `miroms` 数据库）；这里的脚本作为历史版本保留，其中少量脚本（如 `XFUFullMisses.py`）仍会读取本地 `data/devices/*.json`。
> Status: the crawler / exporter scripts have been consolidated into `scripts/` of the [miroms](https://github.com/HegeKen/miroms) repository (sharing the same `miroms` database). Scripts here are kept as a historical version; a few of them (e.g. `XFUFullMisses.py`) still read the local `data/devices/*.json`.

## 迁移说明 | Migration Notice

数据统一迁往 [miroms](https://github.com/HegeKen/miroms)（即 `https://api.miuier.com`，`api/v1` 即 NuxtMR 站点接口）。迁移后数据「以库为准」，由 `scripts/exporter.py` 从 MySQL 重生成，**不要在 `api/v1` 里手改 JSON**；本仓库的 `data/` 只用于回溯与首次播种的对照。

The data now lives in the [miroms](https://github.com/HegeKen/miroms) repository (served at `https://api.miuier.com`; `api/v1` is the NuxtMR site API). After migration the database is the single source of truth: files are regenerated from MySQL by `scripts/exporter.py`, so **never hand-edit JSON in `api/v1`**. `data/` here is only kept for traceability and for verifying the initial seeding.

### 路径对照 | Path mapping

| 本仓库路径 | 迁移后 | 状态 / Status |
| --- | --- | --- |
| `data/devices/<codename>.json` | `api/v1/devices/<codename>.json` | 由 `devices` / `branches` / `roms` 表重生成，共 251 个机型（遗留机型由迁移脚本一次性播种）/ regenerated from DB |
| `data/devices.json` | `api/v1/devices.json` | 手写目录（品牌 → 系列 → 机型顺序，`android` / `miui` 由脚本回填）/ hand-maintained catalog |
| `data/devlist.json` | `api/v1/devlist.json` | 机型列表页 / sitemap 目录，按 `devices/<code>.json` 回填 / regenerated |
| `data/index.json` | `api/v1/index.json` | 首页「本周正式版更新」，按 ISO 周聚合 `roms` / regenerated |
| `data/weekly.json` | `api/v1/weekly.json` | 周更索引，周次取自 `dev` 表（含 MIUIROMS 来源，周数由 54 扩至 353）/ regenerated, weeks may exceed the source files |
| `data/weekly/week-<week>-cn.json` | `api/v1/weekly/week-<week>-cn.json` | 单周公告 + 机型清单 + 日志，来自 `dev` 表与 `roms.dev_week` / regenerated |
| `data/sitelog.json` | `api/v1/sitelog.json` | 站点日志，来自 `sitelog` 表 `site='nuxtmr'` / regenerated |
| `data/tools.json`、`data/thanks.json` | `api/v1/tools.json`、`api/v1/thanks.json` | 手写内容，随 miroms 仓库维护 / hand-maintained |
| `data/log.json`、`stable.json`、`update.json`、`update_full.json`、`newrom.json` | 同名文件 | 废弃脚本的归档产物，仅为兼容旧客户端保留 / archived, kept for old clients |
| `data/devices_template.json`、`weekly_template_*.json`、`list.txt`、`weekly-unfinished.txt` | — | 不迁移（本地模板 / 临时文件）/ not migrated |

### 已知差异 | Known differences

> 迁移后「以库为准」重生成，与原 JSON 存在以下**预期**差异：
>
> - 机型名取自 `devices.full_names`，可能同时包含 POCO 等马甲名（如 `blue` = 「POCO C61 / Redmi A3」）；
> - `dev.bigver` 统一为 `MIUI V6`（V1 周更索引里按历史写法映射回 `MIUI 6`）；
> - 周更机型清单会包含库里 `dev_week` 已绑定但源文件未列出的机型，并去掉源文件里完全重复的行；
> - 周更日志的英文以 `logs` 表里的官方译文为准（源文件是人工翻译）；
> - 周更公告的 `no` / `vid` / `showdevices` / `CnBBSID` / `GbBBSID` 在库里没有对应字段，导出统一为空串 / `"1"`（前端目前都未使用）；
> - 仅存于本仓库、库里没有记录的遗留机型（`data/devices/<codename>.json`）由 `scripts/migrate_v1v2_assets.py` 一次性播种，之后不再自动生成：
>   `HM2013023` / `HM2014011` / `HM2014501` / `camellian` / `cannong` / `ido` / `laurel` / `lcsh92` / `lcsh92_wet_tdd` / `mione` / `pond`。
>
> After migration the data is regenerated from the database, so the differences above are expected. Legacy devices that exist only in this repository are seeded once by `scripts/migrate_v1v2_assets.py` and are not regenerated afterwards.

逐字段说明与迁移脚本见 miroms 仓库 README 的「V1 / V2 附属文件（NuxtMR / HyperOS.fans 站点接口）」「开发版（周更）数据」「站点日志」三节：
<https://github.com/HegeKen/miroms/blob/master/README.md>

Per-field notes and the migration scripts are documented in the miroms README (sections "V1 / V2 附属文件", "开发版（周更）数据", "站点日志"):
<https://github.com/HegeKen/miroms/blob/master/README.md>

### 后续维护 | How to maintain

* **改数据**：在 miroms 仓库操作（先改库 → `python3 scripts/exporter.py` 导出 → 部署 `api.miuier.com`），本仓库 `data/` 不再接收更新。
* **改爬虫**：同样在 miroms 仓库的 `scripts/` 进行；本仓库脚本仅为历史版本。
* **前端取数**：NuxtMR 通过 `API_CONFIG.BASE_URL`（`app/config/api.ts`）请求 `https://api.miuier.com/api/v1`，例如 `devices/<codename>.json`、`weekly.json`、`weekly/week-<week>-cn.json`、`index.json`、`devlist.json`、`sitelog.json`。

* **Data changes**: do them in the miroms repository (update the DB → `python3 scripts/exporter.py` → deploy `api.miuier.com`). `data/` here no longer receives updates.
* **Crawler changes**: also in `scripts/` of the miroms repository; the scripts here are historical.
* **Frontend**: NuxtMR reads `https://api.miuier.com/api/v1` via `API_CONFIG.BASE_URL` (`app/config/api.ts`), e.g. `devices/<codename>.json`, `weekly.json`, `weekly/week-<week>-cn.json`, `index.json`, `devlist.json`, `sitelog.json`.
