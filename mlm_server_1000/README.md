# MLM Server $1000

Сервер с логикой премиальной программы $1000:

- $1000 — стоимость активации партнёра
- $1000 — зелёный бонус за первого личного партнёра
- $500 — зелёный бонус за второго партнёра
- $500 — красный бонус первому партнёру при появлении второго и третьего

## Быстрый старт

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Railway

Переменные окружения:

```
SECRET_KEY=<generate>
DEBUG=False
ALLOWED_HOSTS=*.railway.app
CORE_API_URL=<URL core-сервера>/api
CORE_API_KEY=<API ключ для этого сервера>
SERVER_ID=mlm_server_1000
```

