"""
API views для пользователей
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from users.models import User
from api_gateway.serializers import UserSerializer
from api_gateway.middleware import MLMServerAuthentication


@api_view(['GET'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def get_user(request, user_id):
    """Получить пользователя по ID"""
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def get_user_by_telegram_id(request, telegram_id):
    """Получить пользователя по Telegram ID"""
    try:
        user = User.objects.get(telegram_id=telegram_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def create_user(request):
    """Создать нового пользователя"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def update_user(request, user_id):
    """Обновить данные пользователя"""
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def update_user_status(request, user_id):
    """Обновить статус пользователя в MLM системе"""
    user = get_object_or_404(User, id=user_id)
    mlm_server_id = request.auth.get('server_id') if request.auth else None
    status_value = request.data.get('status')
    
    if not mlm_server_id or not status_value:
        return Response({'error': 'Missing mlm_server_id or status'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.mlm_statuses:
        user.mlm_statuses = {}
    user.mlm_statuses[mlm_server_id] = status_value
    user.save()
    
    return Response({'success': True, 'status': status_value})


@api_view(['POST'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def update_user_rank(request, user_id):
    """Обновить ранг пользователя в MLM системе"""
    user = get_object_or_404(User, id=user_id)
    mlm_server_id = request.auth.get('server_id') if request.auth else None
    rank = request.data.get('rank')
    
    if not mlm_server_id or not rank:
        return Response({'error': 'Missing mlm_server_id or rank'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.mlm_ranks:
        user.mlm_ranks = {}
    user.mlm_ranks[mlm_server_id] = rank
    user.save()
    
    return Response({'success': True, 'rank': rank})

