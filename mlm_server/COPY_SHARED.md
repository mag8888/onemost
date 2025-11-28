# Решение проблемы с модулем shared

## Проблема

Ошибка: `ModuleNotFoundError: No module named 'shared'`

Это происходит, когда Root Directory в Railway установлен на `mlm_server`, а модуль `shared` находится на уровень выше.

## Решение 1: Изменить Root Directory (РЕКОМЕНДУЕТСЯ)

1. В Railway откройте сервис MLM $100
2. Перейдите в **"Settings"** → **"Source"** (или **"Deploy"**)
3. Найдите **"Root Directory"**
4. Измените с `mlm_server` на **пусто** (корень проекта) или `.`
5. Сохраните

**После этого нужно изменить Start Command:**
```bash
cd mlm_server && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:${PORT:-8000}
```

## Решение 2: Использовать PYTHONPATH

Добавьте переменную окружения в Railway:

```env
PYTHONPATH=/app/..:${PYTHONPATH}
```

Где `/app` - это корень проекта в Railway (если Root Directory = mlm_server, то `/app` = mlm_server, а `/app/..` = корень проекта).

## Решение 3: Скопировать shared в mlm_server

Если Root Directory должен быть `mlm_server`, можно скопировать `shared` внутрь:

```bash
cp -r shared mlm_server/
```

Но это не рекомендуется, так как `shared` должен быть общим для всех серверов.

## Текущее решение в коде

Код теперь ищет `shared` в нескольких местах:
- `/app/shared` (если Root Directory = корень)
- `/app/../shared` (если Root Directory = mlm_server)
- `BASE_DIR/shared`
- `BASE_DIR.parent/shared`

## Рекомендация

**Используйте Решение 1** - измените Root Directory на корень проекта и обновите Start Command.

