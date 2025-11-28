"""
API клиент для связи MLM серверов с центральным сервером
"""
import requests
import os
from typing import Dict, Optional, List
from datetime import datetime


class CoreAPIClient:
    """Клиент для взаимодействия с Core Server API"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or os.getenv('CORE_API_URL', 'http://localhost:8000/api')
        self.api_key = api_key or os.getenv('CORE_API_KEY', '')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Выполняет HTTP запрос к Core API"""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            raise
    
    # User methods
    def get_user(self, user_id: int) -> Dict:
        """Получить информацию о пользователе"""
        return self._request('GET', f'/users/{user_id}/')
    
    def create_user(self, user_data: Dict) -> Dict:
        """Создать нового пользователя"""
        return self._request('POST', '/users/', json=user_data)
    
    def update_user(self, user_id: int, user_data: Dict) -> Dict:
        """Обновить данные пользователя"""
        return self._request('PATCH', f'/users/{user_id}/', json=user_data)
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict]:
        """Получить пользователя по Telegram ID"""
        try:
            return self._request('GET', f'/users/telegram/{telegram_id}/')
        except:
            return None
    
    # Wallet methods
    def get_balance(self, user_id: int) -> Dict:
        """Получить баланс пользователя"""
        return self._request('GET', f'/wallet/{user_id}/balance/')
    
    def add_balance(self, user_id: int, amount: float, description: str, 
                   transaction_type: str = 'bonus') -> Dict:
        """Добавить средства на баланс"""
        return self._request('POST', f'/wallet/{user_id}/add/', json={
            'amount': amount,
            'description': description,
            'transaction_type': transaction_type
        })
    
    def withdraw_balance(self, user_id: int, amount: float, 
                        description: str) -> Dict:
        """Списать средства с баланса"""
        return self._request('POST', f'/wallet/{user_id}/withdraw/', json={
            'amount': amount,
            'description': description
        })
    
    # Referral methods
    def register_referral(self, user_id: int, referrer_id: int, 
                         mlm_server_id: str) -> Dict:
        """Зарегистрировать реферальную связь"""
        return self._request('POST', '/referrals/register/', json={
            'user_id': user_id,
            'referrer_id': referrer_id,
            'mlm_server_id': mlm_server_id
        })
    
    def get_referrals(self, user_id: int, mlm_server_id: str) -> List[Dict]:
        """Получить список рефералов пользователя"""
        return self._request('GET', f'/referrals/{user_id}/', params={
            'mlm_server_id': mlm_server_id
        })
    
    def update_user_status(self, user_id: int, status: str, 
                          mlm_server_id: str) -> Dict:
        """Обновить статус пользователя в MLM системе"""
        return self._request('POST', f'/users/{user_id}/status/', json={
            'status': status,
            'mlm_server_id': mlm_server_id
        })
    
    def update_user_rank(self, user_id: int, rank: str, 
                        mlm_server_id: str) -> Dict:
        """Обновить ранг пользователя в MLM системе"""
        return self._request('POST', f'/users/{user_id}/rank/', json={
            'rank': rank,
            'mlm_server_id': mlm_server_id
        })
    
    # Notification methods
    def send_notification(self, user_id: int, message: str, 
                         notification_type: str = 'info') -> Dict:
        """Отправить уведомление пользователю"""
        return self._request('POST', '/notifications/send/', json={
            'user_id': user_id,
            'message': message,
            'notification_type': notification_type
        })

