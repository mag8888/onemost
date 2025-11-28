# Настройка MLM сервера $100 на Railway (ветка 3/100)

## Важно: Root Directory

**Root Directory должен быть:** `mlm_server` (не корень проекта!)

## Переменные окружения

```env
# Django
SECRET_KEY=<сгенерируйте: python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Database (ВАЖНО: используйте DATABASE_PUBLIC_URL!)
DATABASE_PUBLIC_URL=<скопируйте из центрального сервера "onemost">

# Core Server Connection
CORE_API_URL=https://onemost-production.up.railway.app/api
CORE_API_KEY=<скопируйте MLM_SERVER_1_API_KEY из центрального сервера>

# MLM Settings
SERVER_ID=mlm_server_1
```

## Настройка в Railway

### Шаг 1: Создать сервис

1. В Railway создайте новый сервис
2. Выберите **"GitHub Repo"**
3. Репозиторий: `mag8888/onemost`
4. Ветка: **`3/100`**

### Шаг 2: Настроить Root Directory

1. Перейдите в **"Settings"** → **"Source"** (или **"Deploy"**)
2. Найдите **"Root Directory"**
3. Установите: **`mlm_server`**
4. Сохраните

### Шаг 3: Добавить переменные

Добавьте все переменные из списка выше.

### Шаг 4: Проверить Start Command

Railway автоматически использует `railway.json`:
- **Pre-deploy Command**: `python manage.py migrate`
- **Start Command**: `python manage.py runserver`

## Проверка

После настройки:
- ✅ MLM сервер должен собраться
- ✅ Должен подключиться к базе данных
- ✅ Должен подключиться к центральному серверу

## Если ошибка "Error creating build plan"

1. Проверьте, что Root Directory = `mlm_server`
2. Проверьте, что `requirements.txt` существует в `mlm_server/`
3. Проверьте, что `manage.py` существует в `mlm_server/`
4. Перезапустите деплой

