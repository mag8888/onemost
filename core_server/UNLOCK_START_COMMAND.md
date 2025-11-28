# Как разблокировать Start Command в Railway

## Проблема

Поле "Custom Start Command" заблокировано, потому что значение берется из `railway.json`.

## Решение

### Вариант 1: Удалить startCommand из railway.json (рекомендуется)

Railway автоматически использует `railway.json` для всех сервисов. Чтобы разблокировать поле:

1. **Временно удалите** `startCommand` из `railway.json` (или закомментируйте)
2. В Railway настройте команды **вручную** для каждого сервиса:
   - **"onemost"**: `bash start_server.sh`
   - **"onemost-bot"**: `python manage.py run_telegram_bot`
3. После настройки можно вернуть `startCommand` в `railway.json` для основного сервиса

### Вариант 2: Использовать разные конфигурации (сложнее)

Railway не поддерживает разные `railway.json` для разных сервисов напрямую. Но можно:

1. Удалить `startCommand` из `railway.json`
2. Настроить команды вручную в Railway для каждого сервиса
3. Railway запомнит настройки для каждого сервиса отдельно

### Вариант 3: Использовать Procfile (альтернатива)

Создайте `Procfile` в `core_server/`:

```
web: bash start_server.sh
bot: python manage.py run_telegram_bot
```

И в Railway настройте:
- **"onemost"**: процесс `web`
- **"onemost-bot"**: процесс `bot`

## Быстрое решение

### Шаг 1: Временно удалить startCommand

Измените `railway.json` - удалите строку `"startCommand"`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput"
  },
  "deploy": {
    "preDeployCommand": "python manage.py migrate",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Шаг 2: Настроить команды в Railway

1. **Сервис "onemost"**:
   - Settings → Deploy → Custom Start Command: `bash start_server.sh`

2. **Сервис "onemost-bot"**:
   - Settings → Deploy → Custom Start Command: `python manage.py run_telegram_bot`

### Шаг 3: Сохранить и перезапустить

После этого поля разблокируются, и вы сможете настроить команды для каждого сервиса отдельно.

