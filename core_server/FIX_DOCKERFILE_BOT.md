# Исправление: Railway использует Dockerfile вместо railway.json

## Проблема

Railway обнаружил Dockerfile и использует его вместо `railway.json` или `nixpacks.toml`.

В Dockerfile указана команда для веб-сервера:
```dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Поэтому бот не запускается!

## Решение: Переопределить команду в Railway UI

### Вариант 1: Явно указать команду (рекомендуется)

1. Откройте сервис **`onemost-bot`** в Railway
2. Перейдите в **Settings** → **Deploy**
3. Найдите поле **"Custom Start Command"**
4. Введите команду:
   ```bash
   python manage.py migrate --noinput && python manage.py run_telegram_bot
   ```
5. Сохраните изменения

Railway переопределит команду из Dockerfile и запустит бота.

### Вариант 2: Удалить Dockerfile (если не нужен)

Если Dockerfile не используется для других сервисов:

1. Удалите файл `core_server/Dockerfile`
2. Закоммитьте и запушьте изменения
3. Railway будет использовать `railway.json` или `nixpacks.toml`

### Вариант 3: Создать отдельный Dockerfile для бота

Создать `core_server/Dockerfile.bot`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

CMD ["python", "manage.py", "migrate", "--noinput", "&&", "python", "manage.py", "run_telegram_bot"]
```

Но это сложнее, лучше использовать Вариант 1.

## После исправления

1. Railway перезапустит сервис
2. В логах должны появиться:
   ```
   ==================================================
   Initializing Telegram Bot...
   TELEGRAM_BOT_TOKEN exists: True
   ==================================================
   Starting Telegram bot...
   Bot is ready to receive messages
   ```

## Важно!

✅ **Вариант 1 (Custom Start Command) - самый простой и надежный**
✅ Команда в Railway UI переопределяет команду из Dockerfile
✅ Dockerfile останется для веб-сервера (если нужен)

