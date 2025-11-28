"""
API views для MLM
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .services import MLMService


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Зарегистрировать пользователя в MLM системе"""
    user_id = request.data.get('user_id')
    referrer_id = request.data.get('referrer_id')
    
    if not user_id:
        return Response({'error': 'Missing user_id'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = MLMService()
    result = service.register_user(user_id, referrer_id)
    
    if result.get('success'):
        return Response(result, status=status.HTTP_201_CREATED)
    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def upgrade_to_partner(request):
    """Повысить статус до партнера"""
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({'error': 'Missing user_id'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = MLMService()
    result = service.upgrade_to_partner(user_id)
    
    if result.get('success'):
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_rank_upgrade(request):
    """Проверить и повысить ранг"""
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({'error': 'Missing user_id'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = MLMService()
    result = service.check_rank_upgrade(user_id)
    
    return Response(result, status=status.HTTP_200_OK)

