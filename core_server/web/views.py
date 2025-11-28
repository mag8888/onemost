"""
Custom web views for the admin dashboard.
"""
from django.views.generic import TemplateView

from users.models import User, ReferralRelation


class StructureView(TemplateView):
    """Единая админка для просмотра всей структуры."""

    template_name = 'web/structures.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relations'] = (
            ReferralRelation.objects.select_related('user', 'referrer')
            .order_by('mlm_server_id', 'referrer__username', 'user__username')
        )
        context['users'] = User.objects.order_by('-date_joined')
        return context

