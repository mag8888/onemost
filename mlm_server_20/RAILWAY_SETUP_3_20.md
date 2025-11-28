# Настройка MLM сервера $30 на Railway (ветка 3/20)

## Важно: Root Directory

**Root Directory должен быть:** `mlm_server_20` (не корень проекта!)

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
CORE_API_KEY=<скопируйте MLM_SERVER_20_API_KEY из центрального сервера>

# MLM Settings (для программы $30)
MLM_PARTNER_PRICE=30.0
MLM_YELLOW_BONUS=15.0
MLM_GREEN_BONUS=15.0
SERVER_ID=mlm_server_20
```

## Настройка в Railway

### Шаг 1: Создать сервис

1. В Railway создайте новый сервис
2. Выберите **"GitHub Repo"**
3. Репозиторий: `mag8888/onemost`
4. Ветка: **`3/20`**

### Шаг 2: Настроить Root Directory

1. Перейдите в **"Settings"** → **"Source"** (или **"Deploy"**)
2. Найдите **"Root Directory"**
3. Установите: **`mlm_server_20`**
4. Сохраните

### Шаг 3: Добавить переменные

Добавьте все переменные из списка выше.

### Шаг 4: Проверить Start Command

Railway автоматически использует `nixpacks.toml`:
- **Start Command**: `python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:${PORT:-8000}`

## Что исправлено (из опыта 3/100)

- ✅ **Модуль shared** - скопирован внутрь `mlm_server_20/`
- ✅ **nixpacks.toml** - создан для явной конфигурации сборки
- ✅ **PostgreSQL поддержка** - добавлена в `settings.py`
- ✅ **Миграции** - созданы для приложения `mlm`
- ✅ **railway.json** - обновлен для правильной работы
- ✅ **requirements.txt** - добавлены `psycopg2-binary` и `dj-database-url`

## Проверка

После настройки:
- ✅ MLM сервер должен собраться
- ✅ Должен подключиться к базе данных
- ✅ Должен подключиться к центральному серверу
- ✅ Миграции должны примениться автоматически

## Если ошибка "Error creating build plan"

1. Проверьте, что Root Directory = `mlm_server_20`
2. Проверьте, что `requirements.txt` существует в `mlm_server_20/`
3. Проверьте, что `manage.py` существует в `mlm_server_20/`
4. Проверьте, что `nixpacks.toml` существует в `mlm_server_20/`
5. Перезапустите деплой

