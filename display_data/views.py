from django.views.generic import ListView
from .models import ContinentConsumption


class ContinentConsumptionView(ListView):
    model = ContinentConsumption
    template_name = 'display_data/continent_energy_consumption.html'
    context_object_name = 'continent_consumption'
    ordering = ['year']
