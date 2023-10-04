from django.urls import path

from .views import (ContinentConsumptionListView,
                    ContinentConsumptionDetailView,
                    ContinentConsumptionColumnView,
                    CountryConsumptionListView, CountryConsumptionDetailView,
                    CountryConsumptionColumnView,
                    NonRenewablesTotalPowerListView,
                    CountryConsumptionView, )

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
    path('country_energy_consumption/', CountryConsumptionListView.as_view(),
         name='country_consumption'),
    path('country_energy_consumption_detail/<int:pk>/',
         CountryConsumptionDetailView.as_view(),
         name='country_consumption_detail'),
    path('country_energy_consumption_detail/<str:column_name>/',
         CountryConsumptionColumnView.as_view(),
         name='country_energy_consumption_column_detail'),
    path('non_renewables_total_power_generated/',
         NonRenewablesTotalPowerListView.as_view(),
         name='non_renewable_total_power'),
    path('country_energy_consumption_combined.html/',
         CountryConsumptionView.as_view(),
         name='country_consumption_combined'),
]
