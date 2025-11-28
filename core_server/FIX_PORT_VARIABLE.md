# Исправление ошибки с переменной PORT

## Проблема

Ошибка:
```
CommandError: "0.0.0.0:$PORT" is not a valid port number or address:port pair.
```

Это означает, что переменная `$PORT` не подставляется в команду.

## Решение

Django автоматически использует переменную окружения `PORT`, если она установлена. Поэтому не нужно указывать порт в команде.

### Правильная команда:

```bash
python manage.py runserver
```

Django автоматически:
- Использует `PORT` из переменных окружения Railway
- Слушает на `0.0.0.0` (все интерфейсы)
- Использует порт из переменной `PORT`

### Неправильные команды:

❌ `python manage.py runserver 0.0.0.0:$PORT` - переменная не подставляется
❌ `python manage.py runserver 0.0.0.0:${PORT}` - может не работать
❌ `python manage.py runserver 0.0.0.0:8000` - фиксированный порт

## Настройка в Railway

### Сервис "onemost" (веб-сервер):

**Start Command:**
```bash
python manage.py migrate && python manage.py runserver
```

Или используйте `railway.json` (уже исправлен):
- `preDeployCommand`: `python manage.py migrate`
- `startCommand`: `python manage.py runserver`

### Сервис "onemost-bot" (бот):

**Start Command:**
```bash
python manage.py migrate && python manage.py run_telegram_bot
```

## Проверка

После исправления:
- ✅ Веб-сервер должен запуститься на порту из переменной `PORT`
- ✅ Ошибка `CommandError` должна исчезнуть
- ✅ Сервис должен работать корректно

