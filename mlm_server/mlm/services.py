"""
Сервисы MLM системы
"""
import sys
import os
from pathlib import Path

# Добавляем shared в путь
# В Railway, если Root Directory = mlm_server, то /app = mlm_server
# shared находится на уровень выше: /app/../shared
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Список возможных путей к shared
possible_paths = [
    BASE_DIR / 'shared',  # Если Root Directory = корень проекта
    BASE_DIR.parent / 'shared',  # Если Root Directory = mlm_server
    Path('/app') / 'shared',  # Railway: если Root Directory = корень
    Path('/app') / '..' / 'shared',  # Railway: если Root Directory = mlm_server
    Path(__file__).resolve().parent.parent.parent.parent / 'shared',  # Альтернативный путь
]

# Добавляем все возможные пути в sys.path
for shared_path in possible_paths:
    if shared_path.exists() and shared_path.is_dir():
        shared_str = str(shared_path.resolve())
        if shared_str not in sys.path:
            sys.path.insert(0, shared_str)
            break
    # Также добавляем родительскую директорию для поиска
    parent = shared_path.parent
    if parent.exists() and str(parent.resolve()) not in sys.path:
        sys.path.insert(0, str(parent.resolve()))

# Если все еще не найден, добавляем родительскую директорию BASE_DIR
if str(BASE_DIR.parent.resolve()) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent.resolve()))

from shared.api_client import CoreAPIClient
from django.conf import settings
from .models import MLMNode, Bonus
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class MLMService:
    """Сервис для работы с MLM системой"""
    
    def __init__(self):
        self.core_client = CoreAPIClient(
            base_url=settings.CORE_API_URL,
            api_key=settings.CORE_API_KEY
        )
        self.server_id = settings.SERVER_ID
    
    def register_user(self, user_id: int, referrer_id: int = None) -> dict:
        """Зарегистрировать пользователя в MLM системе"""
        try:
            # Получаем информацию о пользователе из Core
            user_data = self.core_client.get_user(user_id)
            
            # Создаем узел в локальной структуре
            node, created = MLMNode.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'referrer_id': referrer_id,
                    'status': 'participant',
                    'rank': '0',
                }
            )
            
            # Регистрируем реферальную связь в Core
            if referrer_id:
                self.core_client.register_referral(
                    user_id=user_id,
                    referrer_id=referrer_id,
                    mlm_server_id=self.server_id
                )
                
                # Размещаем в структуре
                self._place_in_structure(node, referrer_id)
            
            return {'success': True, 'node_id': node.id, 'created': created}
        
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return {'success': False, 'error': str(e)}
    
    def _place_in_structure(self, node: MLMNode, referrer_id: int):
        """Разместить пользователя в структуре (слева направо)"""
        # Находим реферера
        referrer_node = MLMNode.objects.filter(user_id=referrer_id).first()
        if not referrer_node:
            return
        
        # Размещаем слева направо (у пользователя с наименьшим количеством партнеров)
        # Для простоты используем left, center, right
        left_count = MLMNode.objects.filter(referrer_id=referrer_id, position='left').count()
        center_count = MLMNode.objects.filter(referrer_id=referrer_id, position='center').count()
        right_count = MLMNode.objects.filter(referrer_id=referrer_id, position='right').count()
        
        if left_count <= center_count and left_count <= right_count:
            node.position = 'left'
        elif center_count <= right_count:
            node.position = 'center'
        else:
            node.position = 'right'
        
        node.save()
        
        # Обновляем количество партнеров у реферера
        referrer_node.partners_count = MLMNode.objects.filter(referrer_id=referrer_id).count()
        referrer_node.save()
    
    def upgrade_to_partner(self, user_id: int) -> dict:
        """Повысить статус пользователя до партнера"""
        try:
            node = MLMNode.objects.get(user_id=user_id)
            
            if node.status == 'partner':
                return {'success': False, 'error': 'User is already a partner'}
            
            # Обновляем статус
            node.status = 'partner'
            node.save()
            
            # Обновляем в Core
            self.core_client.update_user_status(
                user_id=user_id,
                status='partner',
                mlm_server_id=self.server_id
            )
            
            # Начисляем зеленые бонусы рефереру
            if node.referrer_id:
                self._calculate_green_bonuses(node.referrer_id, user_id)
            
            return {'success': True}
        
        except MLMNode.DoesNotExist:
            return {'success': False, 'error': 'Node not found'}
        except Exception as e:
            logger.error(f"Error upgrading to partner: {e}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_green_bonuses(self, referrer_id: int, new_partner_id: int):
        """Рассчитать зеленые бонусы"""
        referrer_node = MLMNode.objects.filter(user_id=referrer_id).first()
        if not referrer_node or referrer_node.status != 'partner':
            return
        
        # Считаем количество партнеров
        partners = MLMNode.objects.filter(referrer_id=referrer_id, status='partner').count()
        
        if partners == 1:
            # Первый партнер - $100
            amount = Decimal(settings.MLM_GREEN_BONUS_1)
            bonus_type = 'green_1'
        elif partners == 2:
            # Второй партнер - $50
            amount = Decimal(settings.MLM_GREEN_BONUS_2)
            bonus_type = 'green_2'
        else:
            return
        
        # Создаем бонус
        bonus = Bonus.objects.create(
            user_id=referrer_id,
            referrer_id=new_partner_id,
            bonus_type=bonus_type,
            amount=amount,
            description=f'Зеленый бонус за {partners}-го партнера'
        )
        
        # Отправляем в Core
        try:
            self.core_client.add_balance(
                user_id=referrer_id,
                amount=float(amount),
                description=bonus.description,
                transaction_type='mlm_bonus'
            )
            bonus.status = 'sent'
            bonus.save()
        except Exception as e:
            logger.error(f"Error sending bonus to Core: {e}")
            bonus.status = 'failed'
            bonus.save()
        
        # Проверяем красные бонусы
        if partners >= 2:
            self._calculate_red_bonuses(referrer_id)
    
    def _calculate_red_bonuses(self, referrer_id: int):
        """Рассчитать красные бонусы"""
        # Красный бонус - $50 первому партнеру при привлечении 2-го и 3-го
        partners = MLMNode.objects.filter(referrer_id=referrer_id, status='partner').order_by('created_at')
        
        if len(partners) >= 2:
            # Первый партнер получает красный бонус
            first_partner = partners[0]
            
            bonus = Bonus.objects.create(
                user_id=first_partner.user_id,
                referrer_id=referrer_id,
                bonus_type='red',
                amount=Decimal(settings.MLM_RED_BONUS),
                description='Красный бонус за привлечение партнеров'
            )
            
            # Отправляем в Core
            try:
                self.core_client.add_balance(
                    user_id=first_partner.user_id,
                    amount=float(bonus.amount),
                    description=bonus.description,
                    transaction_type='mlm_bonus'
                )
                bonus.status = 'sent'
                bonus.save()
            except Exception as e:
                logger.error(f"Error sending red bonus to Core: {e}")
                bonus.status = 'failed'
                bonus.save()
    
    def check_rank_upgrade(self, user_id: int) -> dict:
        """Проверить и повысить ранг пользователя"""
        try:
            node = MLMNode.objects.get(user_id=user_id)
            
            if node.partners_count >= 3:
                # Повышаем ранг
                current_rank = node.rank
                if current_rank == '0':
                    new_rank = 'ПУ1'
                elif current_rank.startswith('ПУ'):
                    rank_num = int(current_rank.replace('ПУ', ''))
                    new_rank = f'ПУ{rank_num + 1}'
                else:
                    new_rank = 'ПУ1'
                
                node.rank = new_rank
                node.save()
                
                # Обновляем в Core
                self.core_client.update_user_rank(
                    user_id=user_id,
                    rank=new_rank,
                    mlm_server_id=self.server_id
                )
                
                return {'success': True, 'new_rank': new_rank}
            
            return {'success': False, 'message': 'Not enough partners'}
        
        except MLMNode.DoesNotExist:
            return {'success': False, 'error': 'Node not found'}
        except Exception as e:
            logger.error(f"Error checking rank upgrade: {e}")
            return {'success': False, 'error': str(e)}

