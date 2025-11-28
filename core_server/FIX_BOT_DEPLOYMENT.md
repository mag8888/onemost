# Исправление деплоя бота

## Проблемы, которые были найдены:

1. ❌ **`railway.json` содержит команду для веб-сервера** вместо бота
2. ❌ **Отсутствует `DATABASE_URL`** в переменных окружения

## Что исправлено:

### 1. Обновлён `railway.json`
Команда запуска изменена с:
```json
"startCommand": "python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT"
```

На:
```json
"startCommand": "python manage.py migrate && python manage.py run_telegram_bot"
```

### 2. Обновлён `nixpacks.toml`
Команда запуска изменена аналогично.

## Что нужно сделать в Railway:

### 1. Добавить `DATABASE_URL` (критично!)

**Вариант А: Использовать Reference (рекомендуется)**
1. В настройках сервиса `onemost-bot` → Variables
2. Нажмите **"+ New Variable"**
3. Имя: `DATABASE_URL`
4. В поле значения выберите **"Reference"**
5. Выберите ваш PostgreSQL сервис
6. Выберите переменную `DATABASE_URL` или `DATABASE_PUBLIC_URL`
7. Сохраните

**Вариант Б: Скопировать значение вручную**
1. Откройте PostgreSQL сервис в Railway
2. Перейдите в Variables
3. Скопируйте значение `DATABASE_URL` или `DATABASE_PUBLIC_URL`
4. В сервисе `onemost-bot` → Variables
5. Добавьте новую переменную `DATABASE_URL` со скопированным значением

### 2. Проверить Start Command

После пуша изменений Railway должен автоматически обновить команду запуска. Но можно проверить вручную:

1. Откройте сервис `onemost-bot` → Settings → Deploy
2. Проверьте поле **"Custom Start Command"**
3. Должно быть: `python manage.py migrate && python manage.py run_telegram_bot`
4. Если нет - введите вручную и сохраните

## После исправления:

1. **Закоммитьте изменения:**
   ```bash
   git add core_server/railway.json core_server/nixpacks.toml
   git commit -m "Fix: Update start command for bot service"
   git push
   ```

2. **Добавьте `DATABASE_URL` в Railway** (см. выше)

3. **Перезапустите сервис** в Railway

4. **Проверьте логи** - должны быть:
   ```
   Operations to perform:
     Apply all migrations: ...
   Running migrations:
     ...
   Starting Telegram bot...
   Bot is ready to receive messages
   ```

## Проверка работы:

1. Откройте логи сервиса `onemost-bot` в Railway
2. Не должно быть ошибок о подключении к базе данных
3. Должны быть сообщения о запуске бота
4. Проверьте бота в Telegram - отправьте `/start`

