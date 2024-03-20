from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

# models
from services.models import Product, Service, ActionLogs, Location, Datacenter, PCloud, SCloud

class Index(TemplateView):
    """
    online services, wallet, last actions, invoices, last tickets, profile
    """
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # obj = super().get_context_data(**kwargs)
        context = dict()
        context['active_services'] = self.request.user.service_set.filter(status='active')
        context['answered_tickets'] = self.request.user.ticket_set.all()[:7]
        context['last_7actions'] = 'A1'

        print(self.request.user.service_set.filter(status='active').first().scloud.product_cloud.name)
        return context

