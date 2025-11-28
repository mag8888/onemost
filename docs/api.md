# API Документация

## Core Server API

### Аутентификация

Все запросы от MLM серверов должны включать заголовок:
```
Authorization: Bearer {API_KEY}
```

### Endpoints

#### Users

**GET /api/users/{user_id}/**
Получить пользователя по ID

**GET /api/users/telegram/{telegram_id}/**
Получить пользователя по Telegram ID

**POST /api/users/**
Создать нового пользователя
```json
{
  "telegram_id": 123456789,
  "username": "user123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**PATCH /api/users/{user_id}/update/**
Обновить данные пользователя

**POST /api/users/{user_id}/status/**
Обновить статус пользователя в MLM системе
```json
{
  "status": "partner"
}
```

**POST /api/users/{user_id}/rank/**
Обновить ранг пользователя
```json
{
  "rank": "ПУ1"
}
```

#### Wallet

**GET /api/wallet/{user_id}/balance/**
Получить баланс пользователя

**POST /api/wallet/{user_id}/add/**
Добавить средства на баланс
```json
{
  "amount": 100.0,
  "description": "MLM бонус",
  "transaction_type": "mlm_bonus"
}
```

**POST /api/wallet/{user_id}/withdraw/**
Списать средства с баланса

#### Referrals

**POST /api/referrals/register/**
Зарегистрировать реферальную связь
```json
{
  "user_id": 1,
  "referrer_id": 2,
  "mlm_server_id": "mlm_server_1"
}
```

**GET /api/referrals/{user_id}/?mlm_server_id={server_id}**
Получить список рефералов

**GET /api/referrals/{user_id}/link/?mlm_server_id={server_id}**
Получить реферальную ссылку

#### Notifications

**POST /api/notifications/send/**
Отправить уведомление
```json
{
  "user_id": 1,
  "message": "Ваш баланс пополнен",
  "notification_type": "info"
}
```

## MLM Server API

### Endpoints

**POST /api/register/**
Зарегистрировать пользователя в MLM системе
```json
{
  "user_id": 1,
  "referrer_id": 2
}
```

**POST /api/upgrade-partner/**
Повысить статус до партнера
```json
{
  "user_id": 1
}
```

**POST /api/check-rank/**
Проверить и повысить ранг
```json
{
  "user_id": 1
}
```

**GET /api/get-structure/?user_id={user_id}**
Получить структуру рефералов

