from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from services.models import SCloud


class CloudsList(ListView):
    template_name = 'clouds/clouds-list.html'
    context_object_name = 'clouds'

    def get_queryset(self) -> QuerySet[Any]:
        return SCloud.objects.filter(user=self.request.user)
    

class CloudDetail(DetailView):
    model = SCloud
    template_name = 'clouds/cloud-detail.html'
    context_object_name = 'cloud'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        obj = super().get_context_data(**kwargs)
        # get data from datacenter
        obj['installed_os'] = 'ubuntu'
        obj['ipv4'] = '8.8.8.8'
        obj['ipv6'] = '--'
        obj['status'] = 'ubuntu'
        return obj
