"""
Middleware для проверки API ключей MLM серверов
"""
from django.http import JsonResponse
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MLMServerAuthentication(BaseAuthentication):
    """Аутентификация MLM серверов по API ключу"""
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None
        
        api_key = auth_header.split('Bearer ')[1]
        
        # Проверяем ключ в настройках
        for server_id, key in settings.MLM_SERVER_API_KEYS.items():
            if key and key == api_key:
                # Возвращаем кортеж (user, auth) - user может быть None для серверной аутентификации
                return (None, {'server_id': server_id, 'api_key': api_key})
        
        raise AuthenticationFailed('Invalid API key')
    
    def authenticate_header(self, request):
        return 'Bearer'

