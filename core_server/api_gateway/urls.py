"""
API Gateway URLs
"""
from django.urls import path
from api_gateway.views import users, wallet, referrals, notifications

urlpatterns = [
    # Users
    path('users/<int:user_id>/', users.get_user, name='get_user'),
    path('users/telegram/<int:telegram_id>/', users.get_user_by_telegram_id, name='get_user_by_telegram'),
    path('users/', users.create_user, name='create_user'),
    path('users/<int:user_id>/update/', users.update_user, name='update_user'),
    path('users/<int:user_id>/status/', users.update_user_status, name='update_user_status'),
    path('users/<int:user_id>/rank/', users.update_user_rank, name='update_user_rank'),
    
    # Wallet
    path('wallet/<int:user_id>/balance/', wallet.get_balance, name='get_balance'),
    path('wallet/<int:user_id>/add/', wallet.add_balance, name='add_balance'),
    path('wallet/<int:user_id>/withdraw/', wallet.withdraw_balance, name='withdraw_balance'),
    
    # Referrals
    path('referrals/register/', referrals.register_referral, name='register_referral'),
    path('referrals/<int:user_id>/', referrals.get_referrals, name='get_referrals'),
    path('referrals/<int:user_id>/link/', referrals.get_referral_link, name='get_referral_link'),
    
    # Notifications
    path('notifications/send/', notifications.send_notification, name='send_notification'),
]
