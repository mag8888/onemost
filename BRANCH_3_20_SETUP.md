# Настройка ветки 3/20

## Логика сервера $30

### При регистрации нового партнера (оплата $30):

- **$15** → Желтый бонус рефереру
- **$15** → Зеленый бонус рефереру

**Итого:** Реферер получает **$30** за каждого нового партнера.

## Создание ветки

```bash
cd /Users/ADMIN/onemost

# Создаем и переключаемся на ветку 3/20
git checkout -b 3/20

# Добавляем mlm_server_20 и shared
git add mlm_server_20/ shared/

# Коммитим
git commit -m "MLM Server $30: желтый бонус $15 + зеленый бонус $15 за каждого партнера"

# Пушим в ветку 3/20
git push -u origin 3/20
```

## Структура ветки

```
3/20/
├── mlm_server_20/        # MLM сервер с логикой $30
│   ├── mlm/             # MLM логика
│   │   ├── models.py    # Модели (добавлен желтый бонус)
│   │   └── services.py  # Сервисы (логика желтый+зеленый)
│   └── mlm_server/
│       └── settings.py  # Настройки (MLM_YELLOW_BONUS, MLM_GREEN_BONUS)
└── shared/              # Общие модули
```

## Проверка логики

Логика реализована в `mlm_server_20/mlm/services.py`:

```python
def _calculate_yellow_and_green_bonuses(self, referrer_id: int, new_partner_id: int):
    """При регистрации партнера за $30:
    - $15 желтый бонус рефереру
    - $15 зеленый бонус рефереру
    """
```

## Деплой на Railway

1. Создайте новый сервис в Railway
2. Ветка: `3/20`
3. Root Directory: `mlm_server_20`
4. Переменные окружения:
   ```env
   CORE_API_URL=https://your-core.railway.app/api
   CORE_API_KEY=<MLM_SERVER_20_API_KEY из Core>
   SERVER_ID=mlm_server_20
   ```

