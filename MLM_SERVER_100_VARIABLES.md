# Переменные окружения для MLM сервера $100 (ветка 3/100)

## Обязательные переменные

### Django Settings

```env
SECRET_KEY=<сгенерируйте случайный ключ>
```
**Описание:** Секретный ключ Django. Сгенерируйте случайную строку (минимум 50 символов).
**Пример генерации:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

```env
DEBUG=False
```
**Описание:** Режим отладки. В продакшене всегда `False`.

```env
ALLOWED_HOSTS=*.railway.app
```
**Описание:** Разрешенные хосты. Railway автоматически добавляет `*.railway.app`.

### Database (PostgreSQL)

```env
DATABASE_PUBLIC_URL=<скопируйте из центрального сервера>
```
**Описание:** URL базы данных PostgreSQL. Используйте **DATABASE_PUBLIC_URL** из центрального сервера, так как MLM сервер находится в другом проекте Railway.

**Как получить:**
1. Откройте центральный сервер "onemost" в Railway
2. Перейдите в **"Variables"**
3. Найдите `DATABASE_PUBLIC_URL`
4. Скопируйте значение (нажмите на значок глаза, чтобы показать)
5. Вставьте в переменные MLM сервера $100

### Core Server Connection

```env
CORE_API_URL=https://onemost-production.up.railway.app/api
```
**Описание:** URL API центрального сервера. Замените на ваш реальный URL с `/api` в конце.

**Или:**
```env
CORE_SERVER_URL=https://onemost-production.up.railway.app
```
**Описание:** Базовый URL центрального сервера (без `/api`).

```env
CORE_API_KEY=<скопируйте MLM_SERVER_1_API_KEY из центрального сервера>
```
**Описание:** API ключ для связи с центральным сервером. Должен совпадать с `MLM_SERVER_1_API_KEY` в центральном сервере.

**Как получить:**
1. Откройте центральный сервер "onemost" в Railway
2. Перейдите в **"Variables"**
3. Найдите `MLM_SERVER_1_API_KEY`
4. Скопируйте значение
5. Вставьте в переменную `CORE_API_KEY` в MLM сервере $100

### MLM Settings (для программы $100)

```env
SERVER_ID=mlm_server_1
```
**Описание:** Идентификатор сервера. Должен быть `mlm_server_1` для программы $100.

**Примечание:** MLM настройки для $100 (MLM_PARTNER_PRICE, MLM_GREEN_BONUS, MLM_RED_BONUS) обычно задаются в коде сервера, но можно переопределить через переменные окружения, если они поддерживаются.

## Полный список переменных для Railway

```env
# Django
SECRET_KEY=<сгенерируйте: python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Database (из центрального сервера)
DATABASE_PUBLIC_URL=<скопируйте из центрального сервера>

# Core Server Connection
CORE_API_URL=https://onemost-production.up.railway.app/api
CORE_API_KEY=<MLM_SERVER_1_API_KEY из центрального сервера>

# MLM Settings
SERVER_ID=mlm_server_1
```

## Альтернативные названия переменных

В зависимости от кода сервера, могут использоваться разные названия:

```env
# Вместо CORE_API_URL может быть:
CORE_SERVER_URL=https://onemost-production.up.railway.app

# Вместо CORE_API_KEY может быть:
CORE_SERVER_API_KEY=<MLM_SERVER_1_API_KEY>
```

## Важно!

- ✅ **DATABASE_PUBLIC_URL** - используйте публичный URL, так как серверы в разных проектах Railway
- ✅ **CORE_API_KEY** - должен совпадать с `MLM_SERVER_1_API_KEY` в центральном сервере
- ✅ **CORE_API_URL** - URL вашего центрального сервера с `/api` в конце
- ✅ **SERVER_ID** - должен быть `mlm_server_1` для программы $100

## Проверка

После настройки переменных:
1. MLM сервер $100 должен подключиться к базе данных
2. Должен подключиться к центральному серверу
3. Должен обрабатывать MLM логику для программы $100

## Сравнение с MLM сервером $20

| Переменная | MLM $100 | MLM $20 |
|------------|----------|---------|
| SERVER_ID | `mlm_server_1` | `mlm_server_20` |
| CORE_API_KEY | `MLM_SERVER_1_API_KEY` | `MLM_SERVER_20_API_KEY` |
| DATABASE_PUBLIC_URL | Одинаково (из центрального сервера) | Одинаково (из центрального сервера) |
| CORE_API_URL | Одинаково (URL центрального сервера) | Одинаково (URL центрального сервера) |

