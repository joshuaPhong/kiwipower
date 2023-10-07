from django.urls import path

from .views import (ContinentConsumptionListView,
                    ContinentConsumptionDetailView,
                    ContinentConsumptionColumnView,
                    CountryConsumptionListView, CountryConsumptionDetailView,
                    CountryConsumptionColumnView,
                    NonRenewablesTotalPowerListView,
                    CountryConsumptionView, RenewablePowerGenerationListView,
                    RenewablePowerDetailView, RenewablePowerColumnView,
                    RenewablesTotalPowerListView,
                    TopTwentyRenewableCountriesListView,
                    TopTwentyRenewableCountriesDetailView,
                    TopTwentyRenewableCountriesColumnView)

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
    path('renewable_power_generated/',
         RenewablePowerGenerationListView.as_view(), name='renewable_power'),
    path('renewable_power_generated_detail/<int:pk>/',
         RenewablePowerDetailView.as_view(),
         name='renewable_power_detail'),
    path('renewable_power_generated_detail/<str:column_name>/',
         RenewablePowerColumnView.as_view(),
         name='renewable_power_column_detail'),
    path('renewables_total_power_generated/',
         RenewablesTotalPowerListView.as_view(), name='renewables_total_power'),
    path('top_twenty_renewable_countries/',
         TopTwentyRenewableCountriesListView.as_view(),
         name='top_twenty_renewable_countries'),
    path('top_twenty_renewable_countries_detail/<int:pk>/',
         TopTwentyRenewableCountriesDetailView.as_view(),
         name='top_twenty_renewable_countries_detail'),
    path('top_twenty_renewable_countries_column_detail/<str:column_name>/',
         TopTwentyRenewableCountriesColumnView.as_view(),
         name='top_twenty_renewable_countries_column_detail'),

]
