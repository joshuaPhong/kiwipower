# https://www.youtube.com/watch?v=0MrgsYswT1c&list
# =PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2
# reverse generates the URL based on the URL name.
# resolve matches the URL to the corresponding view function.
# self.assertEqual compares the resolved view function with the expected view
# class.
from django.urls import reverse, resolve
from unittest import TestCase
from django.test import SimpleTestCase

from django.urls import reverse

from display_data.views import (ContinentConsumptionListView, \
                                ContinentConsumptionDetailView,
                                ContinentConsumptionColumnView, \
                                CountryConsumptionListView,
                                CountryConsumptionDetailView, \
                                CountryConsumptionColumnView,
                                NonRenewablesTotalPowerListView,
                                RenewablePowerGenerationListView,
                                RenewablePowerDetailView,
                                RenewablePowerColumnView,
                                RenewablesTotalPowerListView)


class UrlsTest(TestCase):
    """
    Test the URLS for the display_data app
    """

    def test_continent_consumption_url(self):
        """
        Test the URL for the ContinentConsumptionListView
        :return:
        """
        url = reverse('continent_consumption')
        self.assertEqual(resolve(url).func.view_class,
                         ContinentConsumptionListView)

    def test_continent_consumption_detail_url(self):
        """
        Test the URL for the ContinentConsumptionDetailView
        :return:
        """
        url = reverse('continent_consumption_detail',
                      args=[1])  # a valid object's primary key
        self.assertEqual(resolve(url).func.view_class,
                         ContinentConsumptionDetailView)

    def test_continent_energy_consumption_column_detail_url(self):
        """
        Test the URL for the ContinentConsumptionColumnView
        :return:
        """
        url = reverse('continent_energy_consumption_column_detail',
                      kwargs={'column_name': 'example_column'})
        self.assertEqual(resolve(url).func.view_class,
                         ContinentConsumptionColumnView)

    def test_country_consumption_url(self):
        """
        Test the URL for the CountryConsumptionListView
        :return: pass or fail
        """
        url = reverse('country_consumption')
        self.assertEqual(resolve(url).func.view_class,
                         CountryConsumptionListView)

    def test_country_consumption_detail_url(self):
        """
        Test the URL for the CountryConsumptionDetailView
        :return: pass or fail
        """
        url = reverse('country_consumption_detail',
                      args=[1])  # a valid object's primary key
        self.assertEqual(resolve(url).func.view_class,
                         CountryConsumptionDetailView)

    def test_country_energy_consumption_column_detail_url(self):
        """
        Test the URL for the CountryConsumptionColumnView
        :return: pass or fail
        """
        url = reverse('country_energy_consumption_column_detail',
                      kwargs={'column_name': 'example_column'})
        self.assertEqual(resolve(url).func.view_class,
                         CountryConsumptionColumnView)

    def test_non_renewable_total_power_url(self):
        """
        Test the url for the NonRenewablesTotalPowerListView
        :return: pass or fail
        """
        url = reverse('non_renewable_total_power')
        self.assertEqual(resolve(url).func.view_class,
                         NonRenewablesTotalPowerListView)

    def test_renewable_power_generated_url(self):
        """
        Test renewable_power_generated_url
        :return: pass or fail
        """
        url = reverse('renewable_power')
        self.assertEqual(resolve(url).func.view_class,
                         RenewablePowerGenerationListView)

    def test_renewable_power_generated_detail_url(self):
        """
        Test renewable_power_generated_detail_url
        :return: pass or fail
        """
        url = reverse('renewable_power_detail',
                      args=[1])  # a valid object's primary key
        self.assertEqual(resolve(url).func.view_class,
                         RenewablePowerDetailView)

    def test_renewable_power_generated_column_url(self):
        """
        Test renewable_power_generated_column_url
        :return: pass or fail
        """
        url = reverse('renewable_power_column_detail',
                      kwargs={'column_name': 'example_column'})
        self.assertEqual(resolve(url).func.view_class,
                         RenewablePowerColumnView)

    def test_renewables_total_power_generated_url(self):
        """
        Test renewable_power_generated_column_url
        :return: pass, error or fail
        """
        url = reverse('renewables_total_power')
        self.assertEqual(resolve(url).func.view_class,
                         RenewablesTotalPowerListView)
