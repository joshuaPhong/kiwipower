from django.views.generic import ListView, DetailView, TemplateView
from .models import ContinentConsumption
import pandas as pd


class ContinentConsumptionListView(ListView):
    model = ContinentConsumption
    template_name = 'display_data/continent_energy_consumption.html'
    context_object_name = 'continent_consumption'
    ordering = ['year']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years = ContinentConsumption.objects.values_list('year', flat=True)
        context['years'] = years
        return context


class ContinentConsumptionDetailView(DetailView):
    model = ContinentConsumption
    template_name = 'display_data/continent_energy_consumption_detail.html'
    context_object_name = 'continent_consumption'


class ContinentConsumptionColumnView(TemplateView):
    pass
