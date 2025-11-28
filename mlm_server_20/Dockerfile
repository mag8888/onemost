FROM python:3.11-slim

WORKDIR /app

# Копирование requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Порт
EXPOSE 8001

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

