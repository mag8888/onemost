# Деплой на Railway

## Подготовка

### 1. Создание проекта на Railway

1. Зайдите на [railway.app](https://railway.app)
2. Создайте новый проект
3. Выберите "Deploy from GitHub repo"

### 2. Структура репозитория

Репозиторий должен иметь следующую структуру веток:
- `centr` - центральный сервер (core_server)
- `3/100` - MLM сервер с логикой $100
- `3/20` - MLM сервер с логикой $20 (опционально)

## Деплой центрального сервера (Core Server)

### Шаг 1: Создание сервиса

1. В Railway создайте новый сервис
2. Подключите репозиторий `https://github.com/mag8888/onemost`
3. Выберите ветку `centr`
4. Укажите корневую директорию: `core_server`

### Шаг 2: Добавление PostgreSQL

1. В том же проекте создайте PostgreSQL базу данных
2. Railway автоматически создаст переменную `DATABASE_URL`

### Шаг 3: Переменные окружения

Добавьте следующие переменные окружения в Railway:

```env
# Django
SECRET_KEY=<сгенерируйте случайный ключ>
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app,*.railway.app

# Database (автоматически из PostgreSQL)
DATABASE_URL=<автоматически>

# Или вручную:
DATABASE_NAME=railway
DATABASE_USER=postgres
DATABASE_PASSWORD=<из Railway>
DATABASE_HOST=<из Railway>
DATABASE_PORT=5432

# Telegram Bot
TELEGRAM_BOT_TOKEN=<ваш токен от @BotFather>
TELEGRAM_WEBAPP_URL=https://your-domain.railway.app

# MLM Server API Keys
MLM_SERVER_1_API_KEY=<сгенерируйте случайный ключ>
MLM_SERVER_2_API_KEY=<сгенерируйте случайный ключ>
MLM_SERVER_20_API_KEY=<сгенерируйте случайный ключ>

# Redis (опционально)
REDIS_URL=<если используете Redis>
```

### Шаг 4: Настройка деплоя

1. В настройках сервиса установите:
   - **Root Directory**: `core_server`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`

### Шаг 5: Запуск бота (отдельный сервис)

1. Создайте еще один сервис в том же проекте
2. Используйте тот же репозиторий и ветку `centr`
3. Root Directory: `core_server`
4. Start Command: `python manage.py run_telegram_bot`
5. Используйте те же переменные окружения

## Деплой MLM сервера ($100)

### Шаг 1: Создание сервиса

1. Создайте новый сервис в Railway
2. Подключите репозиторий `https://github.com/mag8888/onemost`
3. Выберите ветку `3/100`
4. Root Directory: `mlm_server`

### Шаг 2: Переменные окружения

```env
# Django
SECRET_KEY=<сгенерируйте случайный ключ>
DEBUG=False
ALLOWED_HOSTS=your-mlm-domain.railway.app,*.railway.app

# Core Server API
CORE_API_URL=https://your-core-domain.railway.app/api
CORE_API_KEY=<тот же ключ, что MLM_SERVER_1_API_KEY в Core>
SERVER_ID=mlm_server_1
```

### Шаг 3: Настройка деплоя

- **Root Directory**: `mlm_server`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`

## Деплой MLM сервера ($20)

Аналогично MLM серверу $100, но:
- Ветка: `3/20` (или создайте отдельную)
- Root Directory: `mlm_server_20`
- SERVER_ID: `mlm_server_20`
- CORE_API_KEY: используйте `MLM_SERVER_20_API_KEY` из Core

## Проверка деплоя

### Core Server

```bash
# Проверьте доступность
curl https://your-domain.railway.app

# Проверьте API
curl https://your-domain.railway.app/api/users/1/ \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### MLM Server

```bash
# Проверьте доступность
curl https://your-mlm-domain.railway.app

# Проверьте API
curl -X POST https://your-mlm-domain.railway.app/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "referrer_id": null}'
```

## Важные замечания

1. **Домены**: Railway автоматически создает домены для каждого сервиса
2. **Переменные окружения**: Используйте Railway UI для управления переменными
3. **Логи**: Просматривайте логи в Railway Dashboard
4. **Масштабирование**: Railway автоматически масштабирует сервисы
5. **База данных**: PostgreSQL создается автоматически, используйте `DATABASE_URL`

## Обновление кода

1. Закоммитьте изменения в соответствующую ветку
2. Railway автоматически задеплоит изменения
3. Или используйте "Redeploy" в Railway Dashboard

## Мониторинг

- Используйте Railway Dashboard для мониторинга
- Настройте алерты в Railway
- Проверяйте логи регулярно

## Резервное копирование

1. Настройте автоматические бэкапы PostgreSQL в Railway
2. Экспортируйте переменные окружения
3. Сохраните конфигурацию сервисов

