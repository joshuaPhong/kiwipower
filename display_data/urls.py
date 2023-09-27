from django.urls import path

from .views import ContinentConsumptionView

urlpatterns = [
    path('continent_energy_consumption/',
         ContinentConsumptionView.as_view(),
         name='continent_consumption')
]