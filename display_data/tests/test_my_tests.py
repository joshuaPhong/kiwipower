from django.test import TestCase, Client
from display_data.models import ContinentConsumption, \
    NonRenewablesTotalPowerGenerated, \
    CountryConsumption
from django.urls import reverse, resolve
import pandas as pd
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
                                CountryConsumptionView)


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

        self.assertEqual(ContinentConsumption.objects.count(), 1)

    def test_str_method(self):
        """
        Test the __str__ method of ContinentConsumption
        :return:
        """

        self.assertEqual(str(self.continent_consumption), "2023")

    def test_year_field(self):
        """
        Test querying by the 'year' field
        :return:
        """

        queried_instance = ContinentConsumption.objects.filter(
            year=2023).first()
        self.assertEqual(queried_instance, self.continent_consumption)

    def test_continent_fields(self):
        """
        Test querying by individual continent fields
        :return:
        """

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


class TestContinentConsumptionListView(BaseContinentConsumptionTestCase):
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


class TestContinentConsumptionDetailView(BaseContinentConsumptionTestCase):
    """
    Test the ContinentConsumptionDetailView
    """

    def test_continent_consumption_detail_view(self):
        """
        Test the ContinentConsumptionDetailView
        :return: pass, error, or fail
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


class TestContinentConsumptionColumnView(BaseContinentConsumptionTestCase):
    """
    Test the ContinentConsumptionColumnView
    """

    def test_continent_consumption_column_view(self):
        """
        Test the ContinentConsumptionColumnView
        :return: pass or fail
        """
        # Get the URL for the ContinentConsumptionColumnView
        column_name = 'world'
        url = reverse("continent_energy_consumption_column_detail", kwargs={
            'column_name': column_name
        })

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the view returns a 200-status code
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


class BaseClassCountryConsumptionTestCase(TestCase):
    """
    Base class for the CountryConsumption test cases
    """

    def setUp(self):
        """
        Create a sample CountryConsumption instance for testing
        :return:
        """
        self.client = Client()
        self.country_consumption = CountryConsumption.objects.create(
            year=2020,
            china=100.0,
            usa=200.0,
            brazil=300.0,
            belgium=300.0,
            czechia=150.0,
            france=120.0,
            germany=80.0,
            italy=180.0,
            netherlands=60.0,
            poland=90.0,
            portugal=70.0,
            romania=40.0,
            spain=50.0,
            sweden=30.0,
            uk=20.0,
            norway=10.0,
            turkey=5.0,
            kazakhstan=1.0,
            russia=2.0,
            ukraine=3.0,
            uzbeckistan=4.0,
            argentina=5.0,
            canada=6.0,
            chile=7.0,
            colubia=8.0,
            mexico=9.0,
            venezuela=10.0,
            indonesia=11.0,
            japan=12.0,
            malaysia=13.0,
            south_korea=14.0,
            taiwan=15.0,
            thailand=16.0,
            india=17.0,
            australia=18.0,
            new_zealand=19.0,
            algeria=20.0,
            egypt=21.0,
            nigeria=22.0,
            south_africa=23.0,
            iran=24.0,
            kuwait=24.0,
            saudi_arabia=25.0,
            u_a_e=26.0,
        )


class TestCountryConsumptionModel(BaseClassCountryConsumptionTestCase):
    def test_create_country_consumption(self):
        """
        Test creating a CountryConsumption instance
        :return:
        """
        # Test if a CountryConsumption instance can be created and saved
        self.assertEqual(CountryConsumption.objects.count(), 1)
        # Test if the 'year' field is correct
        self.assertEqual(self.country_consumption.year, 2020)

    def test_str_method(self):
        """
        Test the __str__ method of RenewablePowerGenerated
        :return: pass error fail
        """
        self.assertEqual(str(self.country_consumption), "2020")


class TestCountryConsumptionListView(BaseClassCountryConsumptionTestCase):
    def setUp(self):
        self.view_url = reverse(
            'country_consumption')

    def test_view_accessible(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response,
                                'display_data/country_energy_consumption.html')

    def test_view_has_correct_context_data(self):
        # Create a sample object in the database

        response = self.client.get(self.view_url)
        self.assertTrue('country_consumption' in response.context)


class TestCountryConsumptionDetailView(BaseClassCountryConsumptionTestCase):
    def test_country_consumption_detail_view(self):
        """
        Test the ContinentConsumptionDetailView
        :return: pass, error, or fail
        """
        # Get the URL for the ContinentConsumptionDetailView
        url = reverse("country_consumption_detail", args=[
            self.country_consumption.pk])

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the view returns a 200-status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response,
                                "display_data/country_energy_consumption_detail.html")

        # Check if the 'country_consumption' context variable contains the
        # expected object
        self.assertEqual(response.context['country_consumption'],
                         self.country_consumption)


class TestCountryConsumptionColumnView(BaseClassCountryConsumptionTestCase):
    def setUp(self):
        """
        Create a url for testing
        :return:
        """
        self.country_consumption = CountryConsumption.objects.create(
            year=2020,
            china=100.0,
            usa=200.0,
            brazil=300.0,
            belgium=300.0,
            czechia=150.0,
            france=120.0,
            germany=80.0,
            italy=180.0,
            netherlands=60.0,
            poland=90.0,
            portugal=70.0,
            romania=40.0,
            spain=50.0,
            sweden=30.0,
            uk=20.0,
            norway=10.0,
            turkey=5.0,
            kazakhstan=1.0,
            russia=2.0,
            ukraine=3.0,
            uzbeckistan=4.0,
            argentina=5.0,
            canada=6.0,
            chile=7.0,
            colubia=8.0,
            mexico=9.0,
            venezuela=10.0,
            indonesia=11.0,
            japan=12.0,
            malaysia=13.0,
            south_korea=14.0,
            taiwan=15.0,
            thailand=16.0,
            india=17.0,
            australia=18.0,
            new_zealand=19.0,
            algeria=20.0,
            egypt=21.0,
            nigeria=22.0,
            south_africa=23.0,
            iran=24.0,
            kuwait=24.0,
            saudi_arabia=25.0,
            u_a_e=26.0,
        )
        column_name = 'usa'
        self.view_url = reverse('country_energy_consumption_column_detail',
                                kwargs={
                                    'column_name': column_name
                                })

    def test_view_accessible(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response,
                                'display_data'
                                '/country_energy_consumption_column_detail.html')


class TestNonRenewablesTotalPowerListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.view_url = reverse(
            'non_renewable_total_power')
        self.non_renewable_power = (
            NonRenewablesTotalPowerGenerated.objects.create(
                mode_of_generation='example_column',
                contribution_twh=100.0
            ))

    def test_view_accessible(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response,
                                'display_data'
                                '/non_renewables_total_power_generated.html')

    def test_view_has_correct_context_data(self):
        # Create a sample object in the database
        NonRenewablesTotalPowerGenerated.objects.create(
            mode_of_generation='mode_of_generation',
            contribution_twh=100.0
        )

        response = self.client.get(self.view_url)
        self.assertTrue('non_renewables_total_power' in response.context)

    def test_queryset_is_dataframe(self):
        query_set = NonRenewablesTotalPowerGenerated.objects.all()
        df = pd.DataFrame.from_records(query_set.values())
        column_name = 'mode_of_generation'

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertListEqual(list(df.columns),
                             ['id', 'mode_of_generation', 'contribution_twh'])
        self.assertEqual(df.loc[0, 'mode_of_generation'], 'example_column')
        self.assertIn(column_name, df.columns)

    def test_column_data(self):
        query_set = NonRenewablesTotalPowerGenerated.objects.all()
        df = pd.DataFrame.from_records(query_set.values())
        column_name = 'mode_of_generation'
        response = self.client.get(self.view_url,
                                   kwargs={'column_name': column_name})

        self.assertEqual(df.loc[0, 'mode_of_generation'], 'example_column')
        self.assertIn(column_name, df.columns)
        column_data = df[column_name].values[0]
        self.assertEqual(column_data, 'example_column')
