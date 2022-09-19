# 開放台灣民間租屋資料

## Prerequisites

- Python3 (tested with 3.10)
- Docker V2:
  - Supports `docker compose` command.
- node 8+
- gdal

### Tracking Upstream Changes

```bash
git remote add upstream https://github.com/g0v/tw-rental-house-data.git
git remote set-url --push upstream no_push
git fetch upstream master --verbose
```

### Installing Geospatial libraries¶

<https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/geolibs/>

On Ubuntu/Debian:

```bash
sudo apt-get install binutils libproj-dev gdal-bin
```

On MacOS:

```bash
```

## Crawler

### Configure Database

Install Python packages:

```make
make python
```

Migrate database:

Add or Overwrite default settings in `backend/backend/settings_local.py`.

```bash
touch backend/backend/settings_local.py
```

```bash
$ make migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, crawlerrequest, rental, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying rental.0001_initial... OK
  Applying rental.0002_add_author_hash... OK
  Applying rental.0003_add_crawled_at... OK
  Applying rental.0004_fill_crawled_at... OK
  Applying rental.0005_add_more_building_type... OK
  Applying crawlerrequest.0001_initial... OK
  Applying crawlerrequest.0002_crawler_stats... OK
  Applying crawlerrequest.0003_automic_next_request... OK
  Applying rental.0006_add_gps... OK
  Applying rental.0007_more_property_type... OK
  Applying rental.0008_support_price_range... OK
  Applying sessions.0001_initial... OK
Installed 3 object(s) from 1 fixture(s)
```

### Cofigure crawler settings

Configure Scrapy settings:

```bash
cp crawler/crawler/settings.sample.py crawler/crawler/settings.py
```

### Start the crawler

```bash
cd crawler

pipenv run scrapy crawl list591 -L INFO
pipenv run scrapy crawl detail591 -L INFO
pipenv run python ../backend/manage.py syncstateful -ts
pipenv run python ../backend/manage.py statscheck
pipenv run python ../backend/manage.py export -p
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

```bash
export NODE_OPTIONS=--openssl-legacy-provider
npm run dev
```
