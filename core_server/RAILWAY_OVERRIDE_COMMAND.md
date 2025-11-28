# Как переопределить Start Command в Railway

## Проблема

Railway использует `startCommand` из `railway.json` для всех сервисов. Но нам нужно:
- **"onemost"** → `bash start_server.sh` (веб-сервер)
- **"onemost-bot"** → `python manage.py run_telegram_bot` (бот)

## Решение: Переопределить в Railway UI

### Шаг 1: Настроить сервис "onemost" (веб-сервер)

1. Откройте сервис **"onemost"** в Railway
2. Перейдите в **"Settings"** → **"Deploy"**
3. Найдите **"Custom Start Command"**
4. Если поле заблокировано - нажмите на иконку разблокировки (если есть)
5. Или удалите значение из `railway.json` временно, настройте в Railway, затем верните
6. Убедитесь, что команда: `bash start_server.sh`
7. Сохраните

### Шаг 2: Настроить сервис "onemost-bot" (бот)

1. Откройте сервис **"onemost-bot"** в Railway
2. Перейдите в **"Settings"** → **"Deploy"**
3. Найдите **"Custom Start Command"**
4. **Переопределите** команду на: `python manage.py run_telegram_bot`
5. Сохраните

### Шаг 3: Проверить

После настройки:
- **"onemost"** должен запускать веб-сервер
- **"onemost-bot"** должен запускать бота

## Альтернатива: Использовать Procfile

Если переопределение не работает, можно использовать `Procfile`:

1. Создайте файл `core_server/Procfile`:
   ```
   web: bash start_server.sh
   bot: python manage.py run_telegram_bot
   ```

2. В Railway настройте:
   - **"onemost"**: процесс `web`
   - **"onemost-bot"**: процесс `bot`

## Важно!

- ✅ `railway.json` содержит команду по умолчанию для веб-сервера
- ✅ В Railway UI можно переопределить команду для каждого сервиса
- ✅ Переопределение в UI имеет приоритет над `railway.json`

