"""
Скрипт инициализации для Railway
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_server.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Применяем миграции
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Создаем суперпользователя, если его нет
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=os.getenv('ADMIN_PASSWORD', 'admin123')
        )
        print("Superuser created: admin / admin123")

