# Быстрый старт

## Установка и запуск

### 1. Клонирование и настройка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd onemost

# Скопируйте пример переменных окружения
cp env.example .env

# Отредактируйте .env файл, укажите:
# - TELEGRAM_BOT_TOKEN (получите у @BotFather)
# - SECRET_KEY (сгенерируйте случайный ключ)
# - API ключи для MLM серверов
```

### 2. Запуск через Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

### 3. Применение миграций

```bash
# Core Server
docker-compose exec core_server python manage.py migrate
docker-compose exec core_server python manage.py createsuperuser

# MLM Server 1
docker-compose exec mlm_server_1 python manage.py migrate

# MLM Server 2
docker-compose exec mlm_server_2 python manage.py migrate
```

### 4. Запуск Telegram бота

```bash
# В отдельном терминале
docker-compose exec core_server python manage.py run_telegram_bot
```

## Доступ к сервисам

- **Core Server**: http://localhost:8000
- **Core Admin**: http://localhost:8000/admin
- **MLM Server 1**: http://localhost:8001
- **MLM Server 2**: http://localhost:8002

## Тестирование API

### Регистрация пользователя в MLM системе

```bash
curl -X POST http://localhost:8001/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "referrer_id": null
  }'
```

### Повышение до партнера

```bash
curl -X POST http://localhost:8001/api/upgrade-partner/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

## Структура проекта

```
onemost/
├── core_server/      # Центральный сервер
├── mlm_server/       # Шаблон MLM сервера
├── shared/           # Общие модули
├── docs/             # Документация
└── docker-compose.yml
```

## Следующие шаги

1. Настройте переменные окружения для продакшна
2. Настройте домены и SSL
3. Добавьте мониторинг и логирование
4. Настройте резервное копирование БД

