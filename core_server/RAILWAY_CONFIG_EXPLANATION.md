# Конфигурация Railway для разных сервисов

## Структура файлов

- **`railway.json`** - для основного сервера "onemost" (веб-сервер)
- **`railway_bot.json`** - для сервиса бота "onemost-bot" (опционально)

## Настройка сервисов в Railway

### Сервис "onemost" (основной сервер)

1. Откройте сервис **"onemost"** в Railway
2. Перейдите в **"Settings"** → **"Deploy"**
3. **Start Command** должен быть:
   ```bash
   python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT
   ```
4. Или используйте `railway.json` (он уже настроен правильно)

### Сервис "onemost-bot" (бот)

1. Откройте сервис **"onemost-bot"** в Railway
2. Перейдите в **"Settings"** → **"Deploy"**
3. **Start Command** должен быть:
   ```bash
   python manage.py migrate && python manage.py run_telegram_bot
   ```
4. Или скопируйте содержимое `railway_bot.json` в настройки Railway

## Важно!

- ✅ **"onemost"** запускает веб-сервер (`runserver`)
- ✅ **"onemost-bot"** запускает бота (`run_telegram_bot`)
- ❌ **НЕ запускайте бота в "onemost"** - это вызовет конфликт!

## Если Railway использует railway.json автоматически

Если Railway автоматически использует `railway.json` для обоих сервисов:

1. В сервисе **"onemost-bot"** переопределите **Start Command** в настройках Railway
2. Установите: `python manage.py run_telegram_bot`
3. Это переопределит значение из `railway.json`

