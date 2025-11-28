"""
API views для кошелька
"""
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from users.models import User
from wallet.models import Wallet, Transaction
from api_gateway.middleware import MLMServerAuthentication


@api_view(['GET'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def get_balance(request, user_id):
    """Получить баланс пользователя"""
    user = get_object_or_404(User, id=user_id)
    wallet, created = Wallet.objects.get_or_create(user=user)
    
    return Response({
        'user_id': user_id,
        'balance': float(wallet.balance),
        'total_earned': float(wallet.total_earned),
        'total_withdrawn': float(wallet.total_withdrawn),
    })


@api_view(['POST'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def add_balance(request, user_id):
    """Добавить средства на баланс"""
    user = get_object_or_404(User, id=user_id)
    wallet, created = Wallet.objects.get_or_create(user=user)
    
    amount = float(request.data.get('amount', 0))
    description = request.data.get('description', '')
    transaction_type = request.data.get('transaction_type', 'bonus')
    mlm_server_id = request.auth.get('server_id') if request.auth else None
    reference_id = request.data.get('reference_id', '')
    
    if amount <= 0:
        return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        wallet.balance += amount
        wallet.total_earned += amount
        wallet.save()
        
        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=transaction_type,
            status='completed',
            description=description,
            mlm_server_id=mlm_server_id,
            reference_id=reference_id,
        )
    
    return Response({
        'success': True,
        'balance': float(wallet.balance),
        'amount_added': amount,
    })


@api_view(['POST'])
@authentication_classes([MLMServerAuthentication])
@permission_classes([AllowAny])
def withdraw_balance(request, user_id):
    """Списать средства с баланса"""
    user = get_object_or_404(User, id=user_id)
    wallet = get_object_or_404(Wallet, user=user)
    
    amount = float(request.data.get('amount', 0))
    description = request.data.get('description', '')
    
    if amount <= 0:
        return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)
    
    if wallet.balance < amount:
        return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        wallet.balance -= amount
        wallet.total_withdrawn += amount
        wallet.save()
        
        Transaction.objects.create(
            wallet=wallet,
            amount=-amount,
            transaction_type='withdrawal',
            status='completed',
            description=description,
        )
    
    return Response({
        'success': True,
        'balance': float(wallet.balance),
        'amount_withdrawn': amount,
    })

