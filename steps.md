# 開放台灣民間租屋資料

## Prerequisites

- Python3 (tested with 3.10)
- Docker V2:
  - Supports `docker compose` command.
- node 8+

## Crawler

### Configure Database

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

### Cofigure crawler settings

Configure Scrapy settings:

```bash
cp crawler/settings.sample.py crawler/settings.py
```

### Start the crawler

```bash
make crawl
```

### Export the dataset

```bash
python backend/manage.py export --help
```

## Frontend

```bash
$ node --version
v18.4.0

$ npm --version
8.16.0
```

Install packages.

```bash
cd ui
npm install
```

launch the web server.

```
export NODE_OPTIONS=--openssl-legacy-provider
npm run dev
```
