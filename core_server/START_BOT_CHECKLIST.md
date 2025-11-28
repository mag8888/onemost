# Чеклист для запуска бота

## ✅ Шаг 1: Основной сервер работает

Основной сервер "onemost" успешно запущен! Видно в логах:
```
INFO Watching for file changes with StatReloader
```

Это означает, что Django веб-сервер работает.

## ✅ Шаг 2: Проверить настройки бота

Перед запуском бота убедитесь:

### В сервисе "onemost-bot":

1. **Root Directory**: `core_server` (не `/core_server/bot`)
2. **Start Command**: `python manage.py migrate && python manage.py run_telegram_bot`
3. **Variables**:
   - ✅ `DATABASE_URL` (Reference к Postgres)
   - ✅ `TELEGRAM_BOT_TOKEN` (токен от @BotFather)
   - ✅ `SECRET_KEY` (тот же, что в "onemost")
   - ✅ `DEBUG=False`
   - ✅ `ALLOWED_HOSTS=*.railway.app`

### В сервисе "onemost":

1. **Root Directory**: `core_server`
2. **Start Command**: `bash start_server.sh` (или через railway.json)
3. **Variables**:
   - ✅ `DATABASE_URL` (Reference к Postgres)
   - ✅ Все остальные переменные

## ✅ Шаг 3: Запустить бота

1. Откройте сервис **"onemost-bot"** в Railway
2. Убедитесь, что сервис **остановлен** (если был запущен)
3. Подождите **30 секунд** (чтобы освободить Telegram API)
4. Нажмите **"Deploy"** или **"Start"**

## ✅ Шаг 4: Проверить логи бота

После запуска в логах должно быть:

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

**БЕЗ ошибок:**
- ❌ `Conflict: terminated by other getUpdates request`
- ❌ `connection to server at "localhost"`
- ❌ `CommandError`

## ✅ Шаг 5: Проверить работу бота

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Бот должен ответить

## Если возникли проблемы

### Конфликт (Conflict):
- Остановите все экземпляры бота
- Подождите 2-3 минуты
- Запустите только "onemost-bot"

### Ошибка подключения к БД:
- Проверьте `DATABASE_URL` в Variables
- Убедитесь, что используется Reference к Postgres

### Бот не отвечает:
- Проверьте `TELEGRAM_BOT_TOKEN`
- Проверьте логи на наличие ошибок

