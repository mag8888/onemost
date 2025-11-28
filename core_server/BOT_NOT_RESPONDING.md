# Бот не отвечает - диагностика

## Проблема

Бот запущен, но не отвечает на команды. Ошибок в логах нет.

## Что проверить

### 1. Проверить логи сервиса "onemost-bot"

**Важно:** Вы показали логи сервиса "onemost" (веб-сервер), а не "onemost-bot" (бот)!

1. Откройте сервис **"onemost-bot"** в Railway
2. Перейдите на вкладку **"Logs"** или **"Deploy Logs"**
3. Проверьте, что там есть логи бота:

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

### 2. Если логов бота нет

Это означает, что бот не запустился. Проверьте:

1. **Start Command** в сервисе "onemost-bot":
   - Должно быть: `python manage.py migrate && python manage.py run_telegram_bot`
   - Или: `python manage.py run_telegram_bot` (если миграции уже применены)

2. **Root Directory**:
   - Должно быть: `core_server`

3. **Status** сервиса:
   - Должен быть "Running" или "Active"
   - Не должен быть "Crashed" или "Stopped"

### 3. Если логи бота есть, но бот не отвечает

#### Проверка 1: Бот получает обновления?

В логах должны быть строки типа:
```
HTTP Request: POST https://api.telegram.org/bot.../getUpdates "HTTP/1.1 200 OK"
```

Если их нет - бот не получает обновления от Telegram.

#### Проверка 2: Правильный токен?

1. Проверьте `TELEGRAM_BOT_TOKEN` в Variables
2. Убедитесь, что токен правильный (от @BotFather)
3. Попробуйте отправить `/start` боту в Telegram

#### Проверка 3: Бот активен в Telegram?

1. Найдите вашего бота в Telegram
2. Убедитесь, что бот не заблокирован
3. Попробуйте отправить `/start`

#### Проверка 4: База данных работает?

Если бот пытается создать пользователя в БД, но БД недоступна:
- Проверьте `DATABASE_URL` в Variables
- Убедитесь, что используется Reference к Postgres

### 4. Добавить больше логирования

Если бот запущен, но не отвечает, добавьте логирование в обработчики команд:

```python
async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /start command from user {update.effective_user.id}")
    # ... остальной код
```

## Решение

### Шаг 1: Проверить логи "onemost-bot"

Откройте логи сервиса **"onemost-bot"**, а не "onemost"!

### Шаг 2: Если бот не запущен

1. Проверьте Start Command
2. Проверьте Root Directory
3. Перезапустите сервис

### Шаг 3: Если бот запущен, но не отвечает

1. Проверьте, что бот получает обновления (логи getUpdates)
2. Проверьте токен
3. Проверьте базу данных
4. Добавьте больше логирования

## Важно!

- ✅ Логи **"onemost"** = веб-сервер (Django runserver)
- ✅ Логи **"onemost-bot"** = бот (Telegram bot)
- ❌ Не путайте логи разных сервисов!

