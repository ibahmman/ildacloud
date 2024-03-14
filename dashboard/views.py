from django.shortcuts import render
from django.views.generic import TemplateView

class Index(TemplateView):
    """
    online services, wallet, last actions, invoices, last tickets, profile
    """
    template_name = 'dashboard/index.html'
