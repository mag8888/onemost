# Инструкция по загрузке в GitHub

## Подготовка

1. Убедитесь, что у вас есть доступ к репозиторию `https://github.com/mag8888/onemost`
2. Инициализируйте git, если еще не сделано

## Шаг 1: Инициализация репозитория

```bash
cd /Users/ADMIN/onemost
git init
git remote add origin https://github.com/mag8888/onemost.git
```

## Шаг 2: Залить центральный сервер в ветку `centr`

```bash
# Создаем и переключаемся на ветку centr
git checkout -b centr

# Добавляем только core_server и необходимые файлы
git add core_server/
git add shared/
git add .gitignore
git add README.md
git add QUICKSTART.md
git add RAILWAY_SETUP.md
git add env.example
git add docker-compose.yml

# Коммитим
git commit -m "Initial commit: Core Server"

# Пушим в ветку centr
git push -u origin centr
```

## Шаг 3: Залить MLM сервер $100 в ветку `3/100`

```bash
# Переключаемся на main/master
git checkout main
# Или создаем новую ветку от main
git checkout -b 3/100

# Добавляем mlm_server и shared
git add mlm_server/
git add shared/

# Коммитим
git commit -m "MLM Server with $100 logic"

# Пушим в ветку 3/100
git push -u origin 3/100
```

## Шаг 4: Залить MLM сервер $20 в ветку `3/20`

```bash
# Создаем новую ветку
git checkout -b 3/20

# Добавляем mlm_server_20
git add mlm_server_20/
git add shared/

# Коммитим
git commit -m "MLM Server with $20 logic"

# Пушим в ветку 3/20
git push -u origin 3/20
```

## Альтернативный способ (если ветки уже существуют)

```bash
# Для centr
git checkout centr
git add core_server/ shared/ .gitignore README.md QUICKSTART.md RAILWAY_SETUP.md env.example docker-compose.yml
git commit -m "Update Core Server"
git push

# Для 3/100
git checkout 3/100
git add mlm_server/ shared/
git commit -m "Update MLM Server $100"
git push

# Для 3/20
git checkout 3/20
git add mlm_server_20/ shared/
git commit -m "Update MLM Server $20"
git push
```

## Проверка

После пуша проверьте на GitHub:
- Ветка `centr` содержит `core_server/`
- Ветка `3/100` содержит `mlm_server/`
- Ветка `3/20` содержит `mlm_server_20/`

