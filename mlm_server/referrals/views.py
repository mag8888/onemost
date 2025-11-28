"""
API views для реферальной системы
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from mlm.models import MLMNode


@api_view(['GET'])
@permission_classes([AllowAny])
def get_structure(request):
    """Получить структуру рефералов"""
    user_id = request.query_params.get('user_id')
    
    if not user_id:
        return Response({'error': 'Missing user_id'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        nodes = MLMNode.objects.filter(referrer_id=user_id).order_by('position', 'created_at')
        structure = [{
            'user_id': node.user_id,
            'position': node.position,
            'status': node.status,
            'rank': node.rank,
            'partners_count': node.partners_count,
        } for node in nodes]
        
        return Response({
            'user_id': user_id,
            'structure': structure,
            'count': len(structure),
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

