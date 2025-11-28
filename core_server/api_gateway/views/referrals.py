"""
API views для реферальной системы
"""
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import User, ReferralLink, ReferralRelation
from api_gateway.middleware import MLMServerAuthentication
import secrets
import string


@api_view(['POST'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def register_referral(request):
    """Зарегистрировать реферальную связь"""
    user_id = request.data.get('user_id')
    referrer_id = request.data.get('referrer_id')
    mlm_server_id = request.auth.get('server_id') if request.auth else request.data.get('mlm_server_id')
    
    if not all([user_id, referrer_id, mlm_server_id]):
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(User, id=user_id)
    referrer = get_object_or_404(User, id=referrer_id)
    
    # Создаем или получаем реферальную связь
    referral_relation, created = ReferralRelation.objects.get_or_create(
        user=user,
        mlm_server_id=mlm_server_id,
        defaults={'referrer': referrer, 'level': 1}
    )
    
    # Создаем реферальную ссылку для реферера, если её нет
    referral_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    ReferralLink.objects.get_or_create(
        user=referrer,
        mlm_server_id=mlm_server_id,
        defaults={'referral_code': referral_code}
    )
    
    return Response({
        'success': True,
        'created': created,
        'user_id': user_id,
        'referrer_id': referrer_id,
        'mlm_server_id': mlm_server_id,
    })


@api_view(['GET'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def get_referrals(request, user_id):
    """Получить список рефералов пользователя"""
    user = get_object_or_404(User, id=user_id)
    mlm_server_id = request.query_params.get('mlm_server_id') or (request.auth.get('server_id') if request.auth else None)
    
    if not mlm_server_id:
        return Response({'error': 'Missing mlm_server_id'}, status=status.HTTP_400_BAD_REQUEST)
    
    referrals = ReferralRelation.objects.filter(
        referrer=user,
        mlm_server_id=mlm_server_id
    ).select_related('user')
    
    referrals_data = [{
        'user_id': ref.user.id,
        'username': ref.user.username,
        'telegram_id': ref.user.telegram_id,
        'level': ref.level,
        'created_at': ref.created_at.isoformat(),
    } for ref in referrals]
    
    return Response({
        'user_id': user_id,
        'mlm_server_id': mlm_server_id,
        'referrals': referrals_data,
        'count': len(referrals_data),
    })


@api_view(['GET'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def get_referral_link(request, user_id):
    """Получить реферальную ссылку пользователя"""
    user = get_object_or_404(User, id=user_id)
    mlm_server_id = request.query_params.get('mlm_server_id') or (request.auth.get('server_id') if request.auth else None)
    
    if not mlm_server_id:
        return Response({'error': 'Missing mlm_server_id'}, status=status.HTTP_400_BAD_REQUEST)
    
    referral_link, created = ReferralLink.objects.get_or_create(
        user=user,
        mlm_server_id=mlm_server_id
    )
    
    if created:
        import secrets
        import string
        referral_link.referral_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        referral_link.save()
    
    return Response({
        'user_id': user_id,
        'mlm_server_id': mlm_server_id,
        'referral_code': referral_link.referral_code,
    })

