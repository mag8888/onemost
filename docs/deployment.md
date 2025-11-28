# Деплой системы

## Локальная разработка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd onemost
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
# Отредактируйте .env файл
```

### 3. Запуск через Docker Compose

```bash
docker-compose up -d
```

### 4. Применение миграций

```bash
# Core Server
docker-compose exec core_server python manage.py migrate
docker-compose exec core_server python manage.py createsuperuser

# MLM Server
docker-compose exec mlm_server_1 python manage.py migrate
docker-compose exec mlm_server_2 python manage.py migrate
```

### 5. Запуск Telegram бота

```bash
docker-compose exec core_server python manage.py run_telegram_bot
```

## Продакшн деплой

### Railway

1. Создайте проект на Railway
2. Добавьте сервисы:
   - Core Server (PostgreSQL)
   - MLM Server 1
   - MLM Server 2
3. Настройте переменные окружения
4. Деплой через Git

### Переменные окружения для продакшна

**Core Server:**
```
DEBUG=False
SECRET_KEY=<strong-secret-key>
DATABASE_URL=<postgres-url>
TELEGRAM_BOT_TOKEN=<bot-token>
MLM_SERVER_1_API_KEY=<api-key-1>
MLM_SERVER_2_API_KEY=<api-key-2>
```

**MLM Server:**
```
CORE_API_URL=https://your-core-server.railway.app/api
CORE_API_KEY=<api-key>
SERVER_ID=mlm_server_1
```

## Мониторинг

- Логи: `docker-compose logs -f`
- Статус: `docker-compose ps`
- Перезапуск: `docker-compose restart`

