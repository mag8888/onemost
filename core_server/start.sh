#!/bin/bash
# Универсальный скрипт запуска для Railway
# Определяет, какой сервис запускать, по переменной окружения SERVICE_TYPE

# Проверяем переменную SERVICE_TYPE (устанавливается в Railway для каждого сервиса)
SERVICE_TYPE=${SERVICE_TYPE:-"web"}

echo "=========================================="
echo "Service type: $SERVICE_TYPE"
echo "=========================================="

# Определяем, какой сервис запускать
if [ "$SERVICE_TYPE" = "bot" ]; then
    echo "Starting Telegram bot..."
    python manage.py run_telegram_bot
else
    echo "Starting web server..."
    # Получаем порт из переменной окружения PORT (Railway автоматически устанавливает)
    PORT=${PORT:-8000}
    python manage.py runserver 0.0.0.0:$PORT
fi

