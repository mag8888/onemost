"""
API views для уведомлений
"""
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import User
from api_gateway.middleware import MLMServerAuthentication
from bot.tasks import send_telegram_message


@api_view(['POST'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def send_notification(request):
    """Отправить уведомление пользователю"""
    user_id = request.data.get('user_id')
    message = request.data.get('message')
    notification_type = request.data.get('notification_type', 'info')
    
    if not user_id or not message:
        return Response({'error': 'Missing user_id or message'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(User, id=user_id)
    
    if user.telegram_id:
        # Отправляем уведомление через Telegram бота
        send_telegram_message.delay(user.telegram_id, message)
    
    return Response({
        'success': True,
        'user_id': user_id,
        'message_sent': bool(user.telegram_id),
    })

