"""
Django settings package initialization
Добавляем shared в sys.path ДО загрузки settings
"""
import sys
from pathlib import Path

# Определяем BASE_DIR (путь к mlm_server_20)
BASE_DIR = Path(__file__).resolve().parent.parent

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
    '/app/shared',
    '/app',
])

# Добавляем пути в sys.path (убираем дубликаты)
seen = set()
for path_str in paths_to_add:
    if path_str and path_str not in seen:
        seen.add(path_str)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
