# Переменные окружения для Telegram бота

## Критически важные переменные (обязательны)

1. **DATABASE_URL** - URL подключения к PostgreSQL базе данных
   - Формат: `postgresql://user:password@host:port/dbname`
   - В Railway: обычно автоматически создаётся при подключении PostgreSQL сервиса
   - **ВАЖНО**: Если используется `DATABASE_PUBLIC_URL`, то `DATABASE_URL` тоже должен быть установлен

2. **TELEGRAM_BOT_TOKEN** - Токен Telegram бота от @BotFather
   - Формат: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

3. **SERVICE_TYPE** - Тип сервиса для запуска
   - Для бота: `bot`
   - Для веб-сервера: `web`

4. **SECRET_KEY** - Секретный ключ Django
   - Генерируется автоматически или можно использовать: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

## MLM Серверы API Keys

5. **MLM_SERVER_1_API_KEY** - API ключ для MLM сервера $100
   - Получается из переменных окружения MLM сервера $100 (ветка `3/100`)

6. **MLM_SERVER_20_API_KEY** - API ключ для MLM сервера $30
   - Получается из переменных окружения MLM сервера $30 (ветка `3/20`)

7. **MLM_SERVER_1000_API_KEY** - API ключ для MLM сервера $1000
   - Получается из переменных окружения MLM сервера $1000 (ветка `3/1000`)

## MLM Программы URLs

8. **MLM_PROGRAM_30_UPGRADE_URL** - URL для обновления статуса на программу $30
   - Формат: `https://your-mlm-server-30.railway.app/api/upgrade-partner/`
   - Получается из Railway URL MLM сервера $30

9. **MLM_PROGRAM_100_UPGRADE_URL** - URL для обновления статуса на программу $100
   - Формат: `https://your-mlm-server-100.railway.app/api/upgrade-partner/`
   - Получается из Railway URL MLM сервера $100

10. **MLM_PROGRAM_1000_UPGRADE_URL** - URL для обновления статуса на программу $1000
    - Формат: `https://your-mlm-server-1000.railway.app/api/upgrade-partner/`
    - Получается из Railway URL MLM сервера $1000

## Опциональные переменные (имеют значения по умолчанию)

11. **DEBUG** - Режим отладки Django
    - По умолчанию: `False`
    - Для продакшена: `False`
    - Для разработки: `True`

12. **ALLOWED_HOSTS** - Разрешённые хосты
    - По умолчанию: `localhost,127.0.0.1`
    - Для Railway: `onemost-production.up.railway.app,onemost.up.railway.app`

13. **TELEGRAM_WEBAPP_URL** - URL веб-приложения Telegram
    - Опционально, используется для Telegram Web App

14. **MLM_PROGRAM_30_DESCRIPTION** - Описание программы $30
    - По умолчанию: "Стартовая программа $30: быстрый вход в систему..."

15. **MLM_PROGRAM_100_DESCRIPTION** - Описание программы $100
    - По умолчанию: "Программа $100: полный набор уроков..."

16. **MLM_PROGRAM_1000_DESCRIPTION** - Описание программы $1000
    - По умолчанию: "Программа $1000: премиальное наставничество..."

## Что нужно добавить в Railway для бота

### Обязательно добавить:

1. ✅ `DATABASE_URL` - скопировать из PostgreSQL сервиса
2. ✅ `MLM_SERVER_1000_API_KEY` - вместо `MLM_SERVER_2_API_KEY`
3. ✅ `MLM_PROGRAM_30_UPGRADE_URL` - URL MLM сервера $30
4. ✅ `MLM_PROGRAM_100_UPGRADE_URL` - URL MLM сервера $100
5. ✅ `MLM_PROGRAM_1000_UPGRADE_URL` - URL MLM сервера $1000

### Удалить (если есть):

- ❌ `MLM_SERVER_2_API_KEY` - больше не используется, заменить на `MLM_SERVER_1000_API_KEY`

## Проверка после добавления переменных

После добавления всех переменных:
1. Перезапустить сервис бота в Railway
2. Проверить логи - не должно быть ошибок о недостающих переменных
3. Проверить, что бот отвечает на команды в Telegram

