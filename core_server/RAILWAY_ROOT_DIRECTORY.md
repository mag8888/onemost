# Правильная настройка Root Directory в Railway

## Важно!

### Для сервиса "onemost-bot":

**Root Directory должен быть:** `core_server`

**НЕ:** `/core_server/bot` ❌
**НЕ:** `core_server/bot` ❌
**НЕ:** `/bot` ❌

## Почему?

1. `manage.py` находится в `core_server/`
2. Команда `python manage.py run_telegram_bot` должна запускаться из `core_server/`
3. Все зависимости (requirements.txt, settings.py) находятся в `core_server/`

## Как исправить:

1. Откройте сервис **"onemost-bot"** в Railway
2. Перейдите в **"Settings"** → **"Deploy"**
3. Найдите **"Root Directory"**
4. Измените на: `core_server`
5. Сохраните

## Для сервиса "onemost" (основной сервер):

**Root Directory:** `core_server` (такой же)

## Проверка:

После исправления:
- Railway найдет `manage.py`
- Команда `python manage.py run_telegram_bot` будет работать
- Бот запустится без ошибок

