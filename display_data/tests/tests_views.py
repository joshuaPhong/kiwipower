import pandas as pd
from django.test import TestCase, Client
from django.urls import reverse

import os
from PIL import Image
import io

import matplotlib.pyplot as plt

from display_data.models import NonRenewablesTotalPowerGenerated, \
    RenewablePowerGenerated, RenewableTotalPowerGenerated


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

        # todo: test plot.failing
        # if column_name:
        #     self.assertTrue('/display_data/images/bar.png' in
        #     response.context)


class TestRenewablePowerGenerationListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.view_url = reverse(
            'renewable_power')
        self.renewable_power = (
            RenewablePowerGenerated.objects.create(
                year=2019,
                hydro=100.0,
                biofuels=100.0,
                solar=100.0,
                geo_thermal=100.0
            ))

    def test_view_accessible(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response,
                                'display_data'
                                '/renewable_power_generated.html')

    def test_view_contains_correct_context_data(self):
        # Access the test client and the URL for the view
        client = self.client
        view_url = self.view_url

        # Send a GET request to the view and store the response
        response = client.get(view_url)

        # Assert that 'renewable_power' is in the context of the response
        self.assertTrue('years' in response.context)

    def test_queryset_is_dataframe(self):
        query_set = RenewablePowerGenerated.objects.all()
        df = pd.DataFrame.from_records(query_set.values())
        column_name = 'hydro'

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertListEqual(list(df.columns),
                             ['id', 'year', 'hydro', 'biofuels', 'solar',
                              'geo_thermal'])
        self.assertEqual(df.loc[0, 'hydro'], 100.0)
        self.assertIn(column_name, df.columns)

    def test_column_data(self):
        query_set = RenewablePowerGenerated.objects.all()
        df = pd.DataFrame.from_records(query_set.values())
        column_name = 'hydro'
        response = self.client.get(self.view_url,
                                   kwargs={'column_name': column_name})

        self.assertEqual(df.loc[0, 'hydro'], 100.0)
        self.assertIn(column_name, df.columns)
        column_data = df[column_name].values[0]
        self.assertEqual(column_data, 100.0)


class TestRenewablePowerDetailView(TestCase):
    def test_renewable_power_detail_view(self):
        """
        Test that the renewable_power_detail view
        :return: pass, error, or fail
        """
        self.client = Client()
        self.renewable_power = (
            RenewablePowerGenerated.objects.create(
                year=2019,
                hydro=100.0,
                biofuels=100.0,
                solar=100.0,
                geo_thermal=100.0
            ))

        # Get the URL for the ContinentConsumptionDetailView
        url = reverse("renewable_power_detail", args=[1])

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the view returns a 200-status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response,
                                "display_data/renewable_power_generated_detail.html")


class TestRenewablePowerColumnView(TestCase):

    def test_renewable_power_column_view(self):
        # Create a sample object in the database
        self.renewable_power = (
            RenewablePowerGenerated.objects.create(
                year=2019,
                hydro=100.0,
                biofuels=100.0,
                solar=100.0,
                geo_thermal=100.0
            ))
        # Create a test client
        self.client = Client()
        # Set the column name
        column_name = 'hydro'
        # Get the URL for the ContinentConsumptionColumnView
        url = reverse("renewable_power_column_detail", kwargs={
            'column_name': column_name
        })

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the view returns a 200-status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response,
                                "display_data"
                                "/renewable_power_column_detail.html")

        # Check if the 'column_data' context variable exists
        self.assertIn('column_data', response.context)

        # todo: this is duplicate code. We should write a function and
        #  import it from a UTILITY file
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

        # todo: test the plot attributes.
        #  plot is dynamically generated.
        #  the plot file changes every time the view is called.
        # Check if the plot has the correct title
        # Check if the plot has the correct x-axis label
        # Check if the plot has the correct y-axis label
        # Check if the plot has a grid
        # self.assertTrue(plot.title == 'Renewable Power Generation')
        # self.assertTrue(plot.xlabel == 'Year')
        # self.assertTrue(plot.ylabel == 'Hydro')
        # self.assertTrue(plot.grid == True)


class TestRenewablesTotalPowerListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.view_url = reverse(
            'renewables_total_power')
        self.renewable_power = (
            RenewableTotalPowerGenerated.objects.create(
                mode_of_generation='hydro',
                contribution_twh=100.0
            ))

    def test_view_accessible(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response,
                                'display_data'
                                '/renewables_total_power_generated.html')

    def test_view_has_correct_context_data(self):
        response = self.client.get(self.view_url)
        self.assertTrue('renewables_total_power' in response.context)

    def test_queryset_is_dataframe(self):
        query_set = RenewableTotalPowerGenerated.objects.all()
        df = pd.DataFrame.from_records(query_set.values())
        column_name = 'mode_of_generation'

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertListEqual(list(df.columns),
                             ['id', 'mode_of_generation', 'contribution_twh'])
        self.assertEqual(df.loc[0, 'mode_of_generation'], 'hydro')
        self.assertIn(column_name, df.columns)

    def test_column_data(self):
        query_set = RenewableTotalPowerGenerated.objects.all()
        df = pd.DataFrame.from_records(query_set.values())
        column_name = 'mode_of_generation'
        response = self.client.get(self.view_url,
                                   kwargs={'column_name': column_name})

        self.assertEqual(df.loc[0, 'mode_of_generation'], 'hydro')
        self.assertIn(column_name, df.columns)
        column_data = df[column_name].values[0]
        self.assertEqual(column_data, 'hydro')

        # todo: test plot
