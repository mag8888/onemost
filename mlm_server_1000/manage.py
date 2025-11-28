#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# Добавляем shared в путь ДО загрузки Django
# В Railway, если Root Directory = mlm_server_20, то /app = mlm_server_20
BASE_DIR = Path(__file__).resolve().parent

# Добавляем все возможные пути к shared в sys.path
paths_to_add = []
try:
    # Пытаемся получить абсолютные пути
    paths_to_add.extend([
        str((BASE_DIR / 'shared').resolve()),
        str((BASE_DIR.parent / 'shared').resolve()),
        str(BASE_DIR.resolve()),
        str(BASE_DIR.parent.resolve()),
    ])
except Exception:
    # Если resolve() не работает, используем строковые пути
    paths_to_add.extend([
        str(BASE_DIR / 'shared'),
        str(BASE_DIR.parent / 'shared'),
        str(BASE_DIR),
        str(BASE_DIR.parent),
    ])

# Добавляем Railway пути
paths_to_add.extend([
    '/app/shared',  # Railway: если Root Directory = mlm_server_20
    '/app',  # Railway root
])

# Добавляем пути в sys.path (убираем дубликаты)
seen = set()
for path_str in paths_to_add:
    if path_str and path_str not in seen:
        seen.add(path_str)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mlm_server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

