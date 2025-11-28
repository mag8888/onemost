# Добавление нового MLM сервера

## Шаги

### 1. Скопируйте шаблон MLM сервера

```bash
cp -r mlm_server mlm_server_3
```

### 2. Обновите настройки

В `mlm_server_3/mlm_server/settings.py`:

```python
SERVER_ID = os.getenv('SERVER_ID', 'mlm_server_3')
```

### 3. Добавьте в docker-compose.yml

```yaml
  # MLM Server 3
  mlm_server_3:
    build:
      context: ./mlm_server_3
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8003
    volumes:
      - ./mlm_server_3:/app
    ports:
      - "8003:8003"
    environment:
      - DEBUG=True
      - CORE_API_URL=http://core_server:8000/api
      - CORE_API_KEY=${MLM_SERVER_3_API_KEY}
      - SERVER_ID=mlm_server_3
    depends_on:
      - core_server
    networks:
      - onemost_network
```

### 4. Добавьте API ключ в Core Server

В `core_server/core_server/settings.py`:

```python
MLM_SERVER_API_KEYS = {
    'mlm_server_1': os.getenv('MLM_SERVER_1_API_KEY', ''),
    'mlm_server_2': os.getenv('MLM_SERVER_2_API_KEY', ''),
    'mlm_server_3': os.getenv('MLM_SERVER_3_API_KEY', ''),  # Новый
}
```

### 5. Обновите .env файл

```bash
MLM_SERVER_3_API_KEY=mlm-server-3-api-key-here
```

### 6. Запустите

```bash
docker-compose up -d mlm_server_3
docker-compose exec mlm_server_3 python manage.py migrate
```

## Готово!

Новый MLM сервер готов к работе. Он будет автоматически синхронизироваться с Core Server через API.

