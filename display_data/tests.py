from django.test import TestCase, Client
from .models import ContinentConsumption
from django.urls import reverse, resolve
import os
from PIL import Image
import io
from .views import (ContinentConsumptionListView,
                    ContinentConsumptionDetailView,
                    ContinentConsumptionColumnView)


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


class ContinentConsumptionModelTest(BaseContinentConsumptionTestCase):
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


class ContinentConsumptionListViewTest(BaseContinentConsumptionTestCase):
    """
    Test the ContinentConsumptionListView
    """

    def test_continent_consumption_list_view(self):
        """
        Test the ContinentConsumptionListView
        :return:
        """
        # Get the URL for the ContinentConsumptionListView
        url = reverse(
            "continent_consumption")

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response,
                                "display_data/continent_energy_consumption.html")

        # Check if the data from the sample objects appears in the response
        # content
        for year in range(2020, 2031):
            self.assertContains(response,
                                str(2023))

        # Check if the 'years' context variable is present in the response
        self.assertIn('years', response.context)


class ContinentConsumptionDetailViewTest(BaseContinentConsumptionTestCase):
    """
    Test the ContinentConsumptionDetailView
    """

    def test_continent_consumption_detail_view(self):
        """
        Test the ContinentConsumptionDetailView
        :return:
        """
        # Get the URL for the ContinentConsumptionDetailView
        url = reverse("continent_consumption_detail", args=[
            self.continent_consumption.pk])

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the view returns a 200-status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response,
                                "display_data/continent_energy_consumption_detail.html")

        # Check if the 'continent_consumption' context variable contains the
        # expected object
        self.assertEqual(response.context['continent_consumption'],
                         self.continent_consumption)


class ContinentConsumptionColumnViewTest(BaseContinentConsumptionTestCase):
    """
    Test the ContinentConsumptionColumnView
    """

    def test_continent_consumption_column_view(self):
        """
        Test the ContinentConsumptionColumnView
        :return:
        """
        # Get the URL for the ContinentConsumptionColumnView
        column_name = 'world'
        url = reverse("continent_energy_consumption_column_detail", kwargs={
            'column_name': column_name
        })  # Replace with the actual URL name

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response,
                                "display_data"
                                "/continent_energy_consumption_column_detail.html")

        # Check if the 'column_data' context variable exists
        self.assertIn('column_data', response.context)

        # Check if the 'plot_path' context variable exists
        self.assertIn('plot_path', response.context)

        # Check if the saved plot image exists and is a valid image
        plot_path = response.context['plot_path']
        self.assertTrue(os.path.exists(plot_path))
        with open(plot_path, 'rb') as img_file:
            img_data = img_file.read()
            img = Image.open(io.BytesIO(img_data))
            self.assertTrue(img.format in (
                'PNG', 'JPEG'))  # Check if the image format is supported


# reverse generates the URL based on the URL name.
# resolve matches the URL to the corresponding view function.
# self.assertEqual compares the resolved view function with the expected view
# class.
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
