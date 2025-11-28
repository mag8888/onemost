# Инструкция по развертыванию на Railway

## 🚀 Быстрый старт

### 1. Подготовка репозитория

Убедитесь, что код находится в правильных ветках:
- `centr` - центральный сервер
- `3/100` - MLM сервер $100
- `3/20` - MLM сервер $20 (опционально)

### 2. Создание проекта на Railway

1. Зайдите на [railway.app](https://railway.app)
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Подключите репозиторий `mag8888/onemost`

## 📦 Деплой Core Server

### Создание сервиса

1. В проекте нажмите "New Service" → "GitHub Repo"
2. Выберите репозиторий и ветку `centr`
3. В настройках:
   - **Root Directory**: `core_server`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`

### Добавление PostgreSQL

1. В том же проекте: "New Service" → "Database" → "PostgreSQL"
2. Railway автоматически создаст переменную `DATABASE_URL`

### Переменные окружения Core Server

Добавьте в настройках сервиса:

```env
SECRET_KEY=<сгенерируйте: python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Telegram
TELEGRAM_BOT_TOKEN=<от @BotFather>
TELEGRAM_WEBAPP_URL=https://your-core.railway.app

# MLM API Keys (сгенерируйте случайные строки)
MLM_SERVER_1_API_KEY=<случайная строка>
MLM_SERVER_2_API_KEY=<случайная строка>
MLM_SERVER_20_API_KEY=<случайная строка>
```

### Запуск Telegram бота

1. Создайте еще один сервис (New Service → GitHub Repo)
2. Ветка: `centr`, Root: `core_server`
3. Start Command: `python manage.py run_telegram_bot`
4. Используйте те же переменные окружения

## 📦 Деплой MLM Server ($100)

1. "New Service" → "GitHub Repo"
2. Ветка: `3/100`
3. Root Directory: `mlm_server`
4. Start Command: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`

### Переменные окружения MLM Server $100

```env
SECRET_KEY=<сгенерируйте>
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Core API (замените на ваш домен Core Server)
CORE_API_URL=https://your-core.railway.app/api
CORE_API_KEY=<тот же, что MLM_SERVER_1_API_KEY в Core>
SERVER_ID=mlm_server_1
```

## 📦 Деплой MLM Server ($20)

Аналогично MLM Server $100, но:
- Ветка: `3/20` (или создайте отдельную ветку)
- Root Directory: `mlm_server_20`
- SERVER_ID: `mlm_server_20`
- CORE_API_KEY: используйте `MLM_SERVER_20_API_KEY` из Core

## ✅ Проверка

### Core Server

1. Откройте домен сервиса в браузере
2. Должна открыться главная страница
3. `/admin/` - админ-панель (создайте суперпользователя через Railway консоль)

### MLM Server

```bash
# Тест регистрации
curl -X POST https://your-mlm.railway.app/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

## 🔧 Полезные команды

### Создание суперпользователя

В Railway Dashboard → Core Server → Settings → Deploy Logs → Run Command:

```bash
python manage.py createsuperuser
```

### Применение миграций

Миграции применяются автоматически при старте, но можно вручную:

```bash
python manage.py migrate
```

## 📊 Структура проекта на Railway

```
Railway Project
├── Core Server (centr branch)
│   ├── PostgreSQL Database
│   └── Telegram Bot Worker
├── MLM Server $100 (3/100 branch)
└── MLM Server $20 (3/20 branch)
```

## 🔐 Безопасность

1. **Никогда не коммитьте** `.env` файлы
2. Используйте сильные `SECRET_KEY`
3. Генерируйте случайные `API_KEY`
4. Используйте `DEBUG=False` в продакшене

## 📝 Чеклист деплоя

- [ ] Создан проект на Railway
- [ ] Подключен GitHub репозиторий
- [ ] Развернут Core Server (ветка `centr`)
- [ ] Добавлена PostgreSQL база данных
- [ ] Настроены все переменные окружения
- [ ] Запущен Telegram бот (отдельный сервис)
- [ ] Развернут MLM Server $100 (ветка `3/100`)
- [ ] Развернут MLM Server $20 (ветка `3/20`)
- [ ] Проверена работа всех сервисов
- [ ] Создан суперпользователь в Core
- [ ] Настроены домены (опционально)

## 🆘 Решение проблем

### Ошибка подключения к базе данных

- Проверьте переменную `DATABASE_URL`
- Убедитесь, что PostgreSQL сервис запущен
- Проверьте, что Core Server и PostgreSQL в одном проекте

### Ошибка API между серверами

- Проверьте `CORE_API_URL` в MLM серверах
- Убедитесь, что `CORE_API_KEY` совпадает
- Проверьте, что Core Server доступен по HTTPS

### Бот не запускается

- Проверьте `TELEGRAM_BOT_TOKEN`
- Убедитесь, что бот запущен как отдельный сервис
- Проверьте логи в Railway Dashboard

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи в Railway Dashboard
2. Убедитесь, что все переменные окружения установлены
3. Проверьте, что код в правильных ветках

