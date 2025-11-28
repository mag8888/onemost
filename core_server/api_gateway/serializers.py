"""
Serializers для API
"""
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'telegram_id', 'first_name', 
            'last_name', 'phone', 'is_active', 'is_partner', 
            'mlm_statuses', 'mlm_ranks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

