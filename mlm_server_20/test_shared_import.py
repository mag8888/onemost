#!/usr/bin/env python
"""Тестовый скрипт для проверки импорта shared"""
import sys
from pathlib import Path

# Добавляем пути
BASE_DIR = Path(__file__).resolve().parent
paths_to_add = [
    str(BASE_DIR / 'shared'),
    str(BASE_DIR.parent / 'shared'),
    '/app/shared',
    '/app',
    str(BASE_DIR),
]

for path_str in paths_to_add:
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

print("sys.path (first 10):")
for p in sys.path[:10]:
    print(f"  {p}")

print("\nChecking paths:")
for path_str in paths_to_add:
    path = Path(path_str)
    exists = path.exists()
    is_dir = path.is_dir() if exists else False
    print(f"  {path_str}: exists={exists}, is_dir={is_dir}")

print("\nTrying to import shared.api_client...")
try:
    from shared.api_client import CoreAPIClient
    print("✅ SUCCESS: shared.api_client imported successfully!")
except ImportError as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()

