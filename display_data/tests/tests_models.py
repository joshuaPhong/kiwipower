from django.db import IntegrityError

from django.test import TestCase, Client
from display_data.models import ContinentConsumption, \
    NonRenewablesTotalPowerGenerated, \
    CountryConsumption, RenewablePowerGenerated, RenewableTotalPowerGenerated
from django.urls import reverse, resolve
import os
from PIL import Image
import io
from display_data.views import (ContinentConsumptionListView,
                                ContinentConsumptionDetailView,
                                ContinentConsumptionColumnView,
                                CountryConsumptionListView,
                                CountryConsumptionDetailView,
                                CountryConsumptionColumnView,
                                NonRenewablesTotalPowerListView,
                                CountryConsumptionView,
                                RenewablesTotalPowerListView,
                                NonRenewablesTotalPowerListView, )


# Common base class with shared setup logic
# all the tests use the same data,so we create this base class to reduce the
# amount of code and to avoid repeating ourselves
class BaseContinentConsumptionTestCase(TestCase):
    """
    Base class for the ContinentConsumption test cases
    """

    def setUp(self):
        """
        Create a sample ContinentConsumption instance for testing
        :return:
        """
        self.client = Client()

        # Create a sample ContinentConsumption instance for testing
        self.continent_consumption = ContinentConsumption.objects.create(
            year=2023,
            world=1000.0,
            oecd=200.0,
            brics=300.0,
            europe=150.0,
            north_america=120.0,
            latin_america=80.0,
            asia=180.0,
            pacific=60.0,
            africa=90.0,
            middle_east=70.0,
            cis=40.0,
        )


class TestContinentConsumptionModel(BaseContinentConsumptionTestCase):
    """
    Test the ContinentConsumption model
    """

    def test_create_continent_consumption(self):
        """
        Test creating a ContinentConsumption instance
        :return:
        """
        # Test if a ContinentConsumption instance can be created and saved
        self.assertEqual(ContinentConsumption.objects.count(), 1)

    def test_str_method(self):
        """
        Test the __str__ method of ContinentConsumption
        :return:
        """
        # Test the __str__ method of ContinentConsumption
        self.assertEqual(str(self.continent_consumption), "2023")

    def test_year_field(self):
        """
        Test querying by the 'year' field
        :return:
        """
        # Test querying by the 'year' field
        queried_instance = ContinentConsumption.objects.filter(
            year=2023).first()
        self.assertEqual(queried_instance, self.continent_consumption)

    def test_continent_fields(self):
        """
        Test querying by individual continent fields
        :return:
        """
        # Test querying by individual continent fields
        queried_instance = ContinentConsumption.objects.filter(
            europe=150.0).first()
        self.assertEqual(queried_instance, self.continent_consumption)

    def test_update_continent_field(self):
        """

        :return:
        """
        # Test updating a continent field
        self.continent_consumption.europe = 200.0
        self.continent_consumption.save()
        updated_instance = ContinentConsumption.objects.get(year=2023)
        self.assertEqual(updated_instance.europe, 200.0)

    def test_delete_continent_consumption(self):
        """
        Test deleting a ContinentConsumption instance
        :return:
        """
        # Test deleting a ContinentConsumption instance
        self.continent_consumption.delete()
        self.assertEqual(ContinentConsumption.objects.count(), 0)


class TestRenewablePowerGeneration(TestCase):
    """
    Test the RenewablePowerGeneration model
    """

    def setUp(self) -> None:
        self.client = Client()
        # Create a sample RenewablePowerGenerated instance for testing
        self.renewable_power = RenewablePowerGenerated.objects.create(
            year=2020,
            hydro=1000.0,
            biofuels=200.0,
            solar=300.0,
            geo_thermal=150.0
        )

    def test_if_the_objects_are_created(self):
        """
        Test if the objects are created
        :return: pass error fail
        """
        self.assertEqual(self.renewable_power.year, 2020)
        self.assertEqual(self.renewable_power.hydro, 1000.0)
        self.assertEqual(self.renewable_power.biofuels, 200.0)
        self.assertEqual(self.renewable_power.solar, 300.0)
        self.assertEqual(self.renewable_power.geo_thermal, 150.0)

    def test_str_method(self):
        """
        Test the __str__ method of RenewablePowerGenerated
        :return: pass error fail
        """
        self.assertEqual(str(self.renewable_power), "2020")

    def test_renewable_power_unique_year(self):
        """
        Test if the objects are unique. Compare the objects with the same
        value
        This test raised no exception first run, will change year in model to
        unique and run again
        :return:
        """

        with self.assertRaises(IntegrityError):
            RenewablePowerGenerated.objects.create(year=2020,
                                                   hydro=1000.0,
                                                   biofuels=200.0,
                                                   solar=300.0,
                                                   geo_thermal=150.0)


class TestRenewablesTotalPowerGeneratedModel(TestCase):
    """
    Test the NonRenewablesTotalPowerGenerated model
    """

    def setUp(self) -> None:
        self.client = Client()
        # Create a sample NonRenewablesTotalPowerGenerated instance for testing
        self.renewable_total_power = (
            RenewableTotalPowerGenerated.objects.create(
                mode_of_generation="hydro",
                contribution_twh=1000.0
            ))

    def test_if_the_objects_are_created(self):
        """
        Test if the objects are created
        :return: pass error fail
        """
        self.assertEqual(self.renewable_total_power.mode_of_generation,
                         "hydro")
        self.assertEqual(self.renewable_total_power.contribution_twh, 1000.0)

    def test_str_method(self):
        """
        Test the __str__ method of NonRenewablesTotalPowerGenerated
        :return: pass error fail
        """
        self.assertEqual(str(self.renewable_total_power), "hydro")


class TestNonRenewablesTotalPowerGenerated(TestCase):
    """
    Test the NonRenewablesTotalPowerGenerated model
    """

    def setUp(self) -> None:
        self.client = Client()
        # Create a sample RenewablesTotalPowerGenerated instance for testing
        self.non_renewable_total_power = (
            RenewableTotalPowerGenerated.objects.create(
                mode_of_generation="coal",
                contribution_twh=1000.0
            ))

    def test_if_the_objects_are_created(self):
        """
        Test if the objects are created
        :return: pass error fail
        """
        self.assertEqual(self.non_renewable_total_power.mode_of_generation,
                         "coal")
        self.assertEqual(self.non_renewable_total_power.contribution_twh,
                         1000.0)

    def test_str_method(self):
        """
        Test the __str__ method of NonRenewablesTotalPowerGenerated
        :return: pass error fail
        """
        # Test the __str__ method of NonRenewablesTotalPowerGenerated coal
        # will be returned from the list
        self.assertEqual(str(self.non_renewable_total_power), "coal")
