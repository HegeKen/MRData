# MRData
## 项目详情| Repository Info

此项目是新版 [MIUI官方ROM仓库](https://github.com/HegeKen/MIUIROMS) ，即 [NuxtMR](https://github.com/HegeKen/NuxtMR)  所使用到的各项组件以及数据的仓库

This repository contains main assets and data used in [NuxtMR](https://github.com/HegeKen/NuxtMR) project， the new version of [MIUIROMS](https://github.com/HegeKen/MIUIROMS) .

### 文件夹详情 | Folder Info

### `assets`

此文件夹是  [NuxtMR](https://github.com/HegeKen/NuxtMR)  所使用到的[MDUI](https://github.com/zdhxiong/mdui)代码以及部分JS库源码。如此分割后，变更CSS和JS部分代码后，无须再次生成网站，即可生效。

This folder contains [MDUI](https://github.com/zdhxiong/mdui) components used in [NuxtMR](https://github.com/HegeKen/NuxtMR) , and other JS libraries . With this seperation, when changes made to the CSS & JS Part , no need for a re-generate of the website.

### `data`

此文件夹是 [NuxtMR](https://github.com/HegeKen/NuxtMR)  所使用到的数据源 ， 全部用JSON文件格式的形式保存。

This folder source data to form [NuxtMR](https://github.com/HegeKen/NuxtMR) , all data is stored in JSON data format.

### `script`

该文件夹为老的爬虫文件，该文件夹里包含我自己尝试成功或失败的Python爬虫脚本，9月末已实现卡刷包抓取，新爬虫脚本在`scripts`文件夹中。

This folder contains old Python codes I used, and I managed to crawl recovery roms late september, new scripts are in `scripts` folder.

### `scripts`

该文件夹里包含我目前在用的爬虫脚本，现可以抓取卡刷包、线刷包。

This folder contains Python codes I'm currently using to get recovery and fastboot roms.
