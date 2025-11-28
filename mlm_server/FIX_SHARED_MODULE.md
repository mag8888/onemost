# Исправление ошибки "No module named 'shared'"

## Проблема

Ошибка: `ModuleNotFoundError: No module named 'shared'`

Это происходит, когда Root Directory в Railway установлен на `mlm_server`, а модуль `shared` находится на уровень выше.

## Решение

### Вариант 1: Изменить Root Directory (рекомендуется)

1. В Railway откройте сервис MLM сервера $100
2. Перейдите в **"Settings"** → **"Source"**
3. Найдите **"Root Directory"**
4. Измените с `mlm_server` на **пусто** (корень проекта)
5. Сохраните

**Или:**

1. В Railway откройте сервис MLM сервера $100
2. Перейдите в **"Settings"** → **"Deploy"**
3. Найдите **"Root Directory"**
4. Измените на: `.` (точка) или оставьте пустым
5. Сохраните

### Вариант 2: Использовать PYTHONPATH

Добавьте переменную окружения:

```env
PYTHONPATH=/app:${PYTHONPATH}
```

Где `/app` - это корень проекта в Railway.

### Вариант 3: Скопировать shared в mlm_server

Если Root Directory должен быть `mlm_server`, можно скопировать `shared` внутрь `mlm_server`:

```bash
cp -r shared mlm_server/
```

Но это не рекомендуется, так как `shared` должен быть общим для всех серверов.

## Рекомендуемое решение

**Измените Root Directory на корень проекта** (пусто или `.`), чтобы `shared` был доступен.

## Проверка

После исправления:
- MLM сервер должен найти модуль `shared`
- Ошибка `ModuleNotFoundError` должна исчезнуть
- Сервер должен запуститься

