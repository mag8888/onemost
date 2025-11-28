# Микро-модульная система MLM

Распределенная система многоуровневого маркетинга с центральным сервером и серверами реферальной системы.

## 🌿 Ветки репозитория

- **`centr`** - Центральный сервер (Core Server)
- **`3/100`** - MLM сервер с логикой $100
- **`3/20`** - MLM сервер с логикой $20 (пропорционально)

## 🏗️ Архитектура

### Центральный сервер (Core Server)
- **Хранение данных пользователей** - централизованная база данных
- **Веб-интерфейс** - админ-панель и пользовательский интерфейс
- **Telegram бот** - взаимодействие с пользователями
- **Баланс и кошелек** - управление финансами
- **API Gateway** - единая точка входа для всех сервисов

### Серверы реферальной системы (MLM Servers)
- **Независимые серверы** - каждый обрабатывает свою часть реферальной структуры
- **Синхронизация с Core** - обмен данными через API
- **MLM логика** - расчет бонусов, рангов, структуры

## 📁 Структура проекта

```
onemost/
├── core_server/          # Центральный сервер
│   ├── users/           # Управление пользователями
│   ├── wallet/          # Баланс и кошелек
│   ├── bot/             # Telegram бот
│   ├── web/             # Веб-интерфейс
│   └── api_gateway/     # API Gateway
├── mlm_server/          # Шаблон сервера реферальной системы
│   ├── mlm/             # MLM логика
│   ├── referrals/       # Реферальная система
│   └── api_client/      # Клиент для связи с Core
├── shared/              # Общие модули
│   ├── api_client/      # API клиент для межсерверного общения
│   ├── models/          # Общие модели данных
│   └── utils/           # Утилиты
├── docker-compose.yml   # Docker Compose конфигурация
└── docs/                # Документация
```

## 🚀 Быстрый старт

См. [QUICKSTART.md](QUICKSTART.md) для подробных инструкций.

### Быстрая установка

```bash
# 1. Клонируйте репозиторий
git clone <repository-url>
cd onemost

# 2. Настройте переменные окружения
cp env.example .env
# Отредактируйте .env файл

# 3. Запустите через Docker
docker-compose up -d

# 4. Примените миграции
docker-compose exec core_server python manage.py migrate
docker-compose exec mlm_server_1 python manage.py migrate
docker-compose exec mlm_server_2 python manage.py migrate

# 5. Создайте суперпользователя
docker-compose exec core_server python manage.py createsuperuser

# 6. Запустите бота
docker-compose exec core_server python manage.py run_telegram_bot
```

## 🔗 API Коммуникация

Серверы общаются через REST API:
- Core Server предоставляет API для MLM серверов
- MLM серверы отправляют данные обратно в Core
- Используется JWT аутентификация для безопасности

## 📚 Документация

- [Архитектура системы](docs/architecture.md)
- [API документация](docs/api.md)
- [Деплой](docs/deployment.md)
- [Добавление нового MLM сервера](docs/adding_mlm_server.md)

## 🔧 Технологии

- **Backend**: Django 5.0+
- **База данных**: PostgreSQL (Core), SQLite (MLM)
- **API**: Django REST Framework
- **Bot**: python-telegram-bot
- **Контейнеризация**: Docker & Docker Compose

## 📝 Лицензия

Проект создан для внутреннего использования.

