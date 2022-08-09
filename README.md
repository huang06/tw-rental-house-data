# 開放台灣民間租屋資料

長期收集各租屋網站、品牌公寓的可公開資訊，清洗後整理成格式統一的資料，供後續有需要的人使用。

- 專案資訊請見 [hackpad](https://g0v.hackpad.tw/Ih7Jp4pUD5y)。
- 爬蟲套件請見 [PyPI](https://pypi.org/project/scrapy-tw-rental-house/)

## 程式使用方式與注意事項

本專案總共分為兩部份：

- 爬蟲本人，只需要 Scrapy 即可使用，不綁資料庫。
  - [原始碼](https://github.com/g0v/tw-rental-house-data/tree/master/scrapy-package)
  - [套件網頁](https://pypi.org/project/scrapy-tw-rental-house/)
- 完整的開放資料流程，包含爬蟲、資料儲存、網頁。
  - [原始碼](https://github.com/g0v/tw-rental-house-data)
  - [網站](https://rentalhouse.g0v.ddio.io)

本專案還在初期開發階段，任何框架、資料庫定義、API 皆有可能更動。

關於開發的詳細資訊，請參見[專案 wiki](https://github.com/g0v/tw-rental-house-data/wiki/)

### 爬蟲本人

關於環境需求與使用方式，請見[套件網頁](https://pypi.org/project/scrapy-tw-rental-house/)。

### 資料庫與網頁後端

#### 爬蟲環境需求

- Python3 (tested with 3.10)
- Docker V2:
  - Supports `docker compose` command.

#### 資料庫設定

Install Python packages:

```make
make python
```

Migrate database:

Add or Overwrite default settings in `backend/settings_local.py`.

```bash
touch backend/settings_local.py
```

```bash
make migrate
```

#### 爬蟲使用方式

確定資料庫準備完成後，執行以下步驟：

Configure Scrapy settings:

```bash
cp crawler/settings.sample.py crawler/settings.py
```

```bash
make crawl
```

#### 資料匯出

```bash
python backend/manage.py export --help
```

#### 注意事項

1. 請友善對待租屋網站，依其個別網站使用規則容許的方式與頻率來查詢資料，建議可使用 Scrapy 內附的
   [DOWNLOAD_DELAY](https://doc.scrapy.org/en/latest/topics/settings.html#std:setting-DOWNLOAD_DELAY) 或
   [AUTO_THROTTLING](https://doc.scrapy.org/en/latest/topics/autothrottle.html) 調整爬蟲速度。
2. 爬蟲以收集各網站可散佈的共同資料欄位為主，不會儲存所有網頁上的欄位。
3. 使用者使用本專案提供程式來進行公開資訊的分析與調取，其使用行為及後續資訊的利用行為，
   需符合現行法令的要求且自負其責，包括但不限於個人隱私、資料保護、資訊安全，以及公平競爭等相關規定。
4. 其他事項請參見[授權頁面](LICENSE)。

### 網頁前端

#### 網頁環境需求

- node 8+

#### 使用方式

```sh
# 安裝套件
cd web/ui
npm install

# 啟動開發環境
npm run dev

```

詳細操作方式，請參見 [nuxt](https://nuxtjs.org/)

## 非宅界專案貢獻者

- [Lucien C.H. Lin (林誠夏)](lucien.cc)
- [勞工陣線](http://labor.ngo.tw/) 洪敬舒
