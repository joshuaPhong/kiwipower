from django.urls import path

from .views import (ContinentConsumptionListView,
                    ContinentConsumptionDetailView,
                    ContinentConsumptionColumnView)

urlpatterns = [
    path('continent_energy_consumption/',
         ContinentConsumptionListView.as_view(),
         name='continent_consumption'),
    path('continent_energy_consumption_detail/<int:pk>/',
         ContinentConsumptionDetailView.as_view(),
         name='continent_consumption_detail'),
    path('continent_energy_consumption_detail/<str:column_name>/',
         ContinentConsumptionColumnView.as_view(),
         name='continent_energy_consumption_column_detail'),
]
