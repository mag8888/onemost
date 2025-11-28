#!/bin/bash
# Скрипт для запуска Django сервера с правильным портом из Railway

# Получаем порт из переменной окружения PORT (Railway автоматически устанавливает)
PORT=${PORT:-8000}

# Запускаем Django сервер
python manage.py runserver 0.0.0.0:$PORT

