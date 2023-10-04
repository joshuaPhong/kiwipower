from django.test import TestCase, Client
from display_data.models import NonRenewablesTotalPowerGenerated
import pandas as pd
from django.urls import reverse
import os
from PIL import Image
import io
from display_data.views import (
    NonRenewablesTotalPowerListView
)


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
