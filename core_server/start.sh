#!/bin/bash
# Универсальный скрипт запуска для Railway
# Определяет, какой сервис запускать, по переменной окружения RAILWAY_SERVICE_NAME

# Получаем имя сервиса из переменной окружения Railway
SERVICE_NAME=${RAILWAY_SERVICE_NAME:-"onemost"}

echo "=========================================="
echo "Starting service: $SERVICE_NAME"
echo "=========================================="

# Определяем, какой сервис запускать
if [ "$SERVICE_NAME" = "onemost-bot" ] || [ "$SERVICE_NAME" = "onemost-bot-production" ]; then
    echo "Starting Telegram bot..."
    python manage.py run_telegram_bot
else
    echo "Starting web server..."
    # Получаем порт из переменной окружения PORT (Railway автоматически устанавливает)
    PORT=${PORT:-8000}
    python manage.py runserver 0.0.0.0:$PORT
fi

