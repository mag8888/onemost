# Переменные окружения для MLM сервера $20 (ветка 3/20)

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
5. Вставьте в переменные MLM сервера $20

### Core Server Connection

```env
CORE_SERVER_URL=https://onemost-production.up.railway.app
```
**Описание:** URL центрального сервера. Замените на ваш реальный URL.

```env
CORE_SERVER_API_KEY=<скопируйте MLM_SERVER_20_API_KEY из центрального сервера>
```
**Описание:** API ключ для связи с центральным сервером. Должен совпадать с `MLM_SERVER_20_API_KEY` в центральном сервере.

**Как получить:**
1. Откройте центральный сервер "onemost" в Railway
2. Перейдите в **"Variables"**
3. Найдите `MLM_SERVER_20_API_KEY`
4. Скопируйте значение
5. Вставьте в переменную `CORE_SERVER_API_KEY` в MLM сервере $20

### MLM Settings (для программы $20)

```env
MLM_PARTNER_PRICE=20.0
```
**Описание:** Цена для получения статуса партнера ($20).

```env
MLM_YELLOW_BONUS=10.0
```
**Описание:** Желтый бонус за регистрацию партнера ($10).

```env
MLM_GREEN_BONUS=10.0
```
**Описание:** Зеленый бонус за регистрацию партнера ($10).

```env
SERVER_ID=mlm_server_20
```
**Описание:** Идентификатор сервера. Должен быть `mlm_server_20`.

## Полный список переменных для Railway

```env
# Django
SECRET_KEY=<сгенерируйте: python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Database (из центрального сервера)
DATABASE_PUBLIC_URL=<скопируйте из центрального сервера>

# Core Server Connection
CORE_SERVER_URL=https://onemost-production.up.railway.app
CORE_SERVER_API_KEY=<MLM_SERVER_20_API_KEY из центрального сервера>

# MLM Settings
MLM_PARTNER_PRICE=20.0
MLM_YELLOW_BONUS=10.0
MLM_GREEN_BONUS=10.0
SERVER_ID=mlm_server_20
```

## Важно!

- ✅ **DATABASE_PUBLIC_URL** - используйте публичный URL, так как серверы в разных проектах Railway
- ✅ **CORE_SERVER_API_KEY** - должен совпадать с `MLM_SERVER_20_API_KEY` в центральном сервере
- ✅ **CORE_SERVER_URL** - URL вашего центрального сервера
- ✅ Все MLM настройки должны быть для $20

## Проверка

После настройки переменных:
1. MLM сервер $20 должен подключиться к базе данных
2. Должен подключиться к центральному серверу
3. Должен обрабатывать MLM логику для программы $20

