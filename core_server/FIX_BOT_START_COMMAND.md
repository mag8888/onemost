# Исправление Start Command для бота

## Проблема

В сервисе "onemost-bot" запускается веб-сервер вместо бота!

В логах видно:
```
INFO Watching for file changes with StatReloader
```

Это Django веб-сервер, а не бот!

## Причина

В сервисе "onemost-bot" установлена неправильная команда:
- ❌ `bash start_server.sh` - это для веб-сервера
- ✅ Должно быть: `python manage.py run_telegram_bot` - это для бота

## Решение

### Шаг 1: Откройте сервис "onemost-bot"

1. В Railway откройте сервис **"onemost-bot"** (не "onemost"!)
2. Перейдите в **"Settings"** → **"Deploy"**

### Шаг 2: Измените Start Command

1. Найдите поле **"Custom Start Command"**
2. Измените с `bash start_server.sh` на:
   ```bash
   python manage.py run_telegram_bot
   ```
3. Или можно оставить Pre-deploy Command для миграций:
   - **Pre-deploy Command**: `python manage.py migrate`
   - **Custom Start Command**: `python manage.py run_telegram_bot`

### Шаг 3: Сохраните и перезапустите

1. Сохраните изменения
2. Railway автоматически перезапустит сервис
3. Проверьте логи - должно быть:

```
==================================================
Initializing Telegram Bot...
TELEGRAM_BOT_TOKEN exists: True
==================================================
Setting up bot... Token exists: True
Creating Telegram application...
Registering command handlers...
Bot setup completed successfully
==================================================
Starting Telegram bot...
Bot is ready to receive messages
==================================================
Bot initialized successfully
Application started
```

**БЕЗ строки** `Watching for file changes with StatReloader`!

## Правильные настройки

### Сервис "onemost" (веб-сервер):
- **Pre-deploy Command**: `python manage.py migrate`
- **Custom Start Command**: `bash start_server.sh` ✅

### Сервис "onemost-bot" (бот):
- **Pre-deploy Command**: `python manage.py migrate` (опционально)
- **Custom Start Command**: `python manage.py run_telegram_bot` ✅

## Важно!

- ✅ **"onemost"** запускает веб-сервер (`bash start_server.sh`)
- ✅ **"onemost-bot"** запускает бота (`python manage.py run_telegram_bot`)
- ❌ **НЕ путайте команды!**

