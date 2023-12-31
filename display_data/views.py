from django.views.generic import ListView, DetailView, TemplateView
from .models import ContinentConsumption, CountryConsumption, \
    NonRenewablesTotalPowerGenerated, RenewablePowerGenerated, \
    RenewableTotalPowerGenerated, TopTwentyRenewableCountries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')


class ContinentConsumptionListView(ListView):
    model = ContinentConsumption
    template_name = 'display_data/continent_energy_consumption.html'
    context_object_name = 'continent_consumption'
    ordering = ['year']
    paginate_by = 10


class ContinentConsumptionDetailView(DetailView):
    model = ContinentConsumption
    template_name = 'display_data/continent_energy_consumption_detail.html'
    context_object_name = 'continent_consumption'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the object
        continent_consumption = self.get_object()

        # Get a list of all field names in the model (excluding id and year)
        field_names = [field.name for field in
                       ContinentConsumption._meta.get_fields()][3:]  # remove
        # id year and world

        # Extract the data values for all fields dynamically
        data = [getattr(continent_consumption, field_name) for field_name in
                field_names]

        # Create a list of tuples with (field_name, value) pairs
        data_with_names = list(zip(field_names, data))

        # Calculate the highest and lowest values in the row
        min_pair = min(data_with_names, key=lambda x: x[1])
        max_pair = max(data_with_names, key=lambda x: x[1])

        # Add the min and max values and their corresponding field names to
        # the context
        context['min_value'] = min_pair[1]
        context['max_value'] = max_pair[1]
        context['min_continent'] = min_pair[0]
        context['max_continent'] = max_pair[0]

        return context


class ContinentConsumptionColumnView(TemplateView):
    template_name = ('display_data/continent_energy_consumption_column_detail'
                     '.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        column_name = self.kwargs.get('column_name', None)

        if column_name:
            queryset = ContinentConsumption.objects.all()
            continent_consumption = pd.DataFrame.from_records(
                queryset.values())
            # mine
            column_data = continent_consumption[column_name]
            context['column_data'] = column_data
            # mine
            column_year = continent_consumption['year']
            context['column_year'] = column_year

            # gpt.
            # I wanted both the year and the data in the same list
            # Combine values and years into a list of tuples
            column_data_and_year = list(zip(column_year, column_data))
            context['column_data_and_year'] = column_data_and_year

            #     create a plot
            plt.figure(figsize=(10, 5))
            plt.plot(continent_consumption['year'], column_data)
            plt.xlabel('Year')
            plt.ylabel(column_name)
            plt.title(f'{column_name} by Year')
            plt.grid(True)

            # save img
            plot_path = 'static/display_data/images/plot.png'
            plt.savefig(plot_path)
            plt.close()

            context['plot_path'] = plot_path

        return context


class CountryConsumptionListView(ListView):
    model = CountryConsumption
    template_name = 'display_data/country_energy_consumption.html'
    context_object_name = 'country_consumption'
    ordering = ['year']
    paginate_by = 10


class CountryConsumptionDetailView(DetailView):
    model = CountryConsumption
    template_name = 'display_data/country_energy_consumption_detail.html'
    context_object_name = 'country_consumption'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the object
        country_consumption = self.get_object()

        # Get a list of all field names in the model (excluding id and year)
        field_names = [field.name for field in
                       CountryConsumption._meta.get_fields()][2:]

        # Extract the data values for all fields dynamically
        data = [getattr(country_consumption, field_name) for field_name in
                field_names]

        # Create a list of tuples with (field_name, value) pairs
        data_with_names = list(zip(field_names, data))

        # Calculate the highest and lowest values in the row
        min_pair = min(data_with_names, key=lambda x: x[1])
        max_pair = max(data_with_names, key=lambda x: x[1])

        # Add the min and max values and their corresponding field names to
        # the context
        context['min_value'] = min_pair[1]
        context['max_value'] = max_pair[1]
        context['min_country'] = min_pair[0]
        context['max_country'] = max_pair[0]

        return context


class CountryConsumptionColumnView(TemplateView):
    template_name = ('display_data/country_energy_consumption_column_detail'
                     '.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        column_name = self.kwargs.get('column_name', None)

        if column_name:
            queryset = CountryConsumption.objects.all().order_by('year')
            country_consumption = pd.DataFrame.from_records(
                queryset.values())

            column_data = country_consumption[column_name]
            context['column_data'] = column_data

            #     create a plot
            plt.figure(figsize=(10, 5))
            plt.plot(country_consumption['year'], column_data)
            plt.xlabel('Year')
            plt.ylabel(f'{column_name}(TWh)')
            plt.title(f'{column_name} by Year (TWh)')
            plt.grid(True)

            # save img
            plot_path = 'static/display_data/images/plot.png'
            plt.savefig(plot_path)
            plt.close()

            context['plot_path'] = plot_path

        return context


class NonRenewablesTotalPowerListView(ListView):
    model = NonRenewablesTotalPowerGenerated
    template_name = 'display_data/non_renewables_total_power_generated.html'
    context_object_name = 'non_renewables_total_power'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        template_name = self.template_name
        context['template_name'] = template_name

        queryset = NonRenewablesTotalPowerGenerated.objects.all()
        non_renewable_power = pd.DataFrame.from_records(
            queryset.values())

        # Create a bar graph
        plt.figure(figsize=(10, 6))
        plt.bar(non_renewable_power['mode_of_generation'],
                non_renewable_power['contribution_twh'],
                color='skyblue')
        plt.xlabel('Mode of Generation')
        plt.ylabel('Contribution (TWh)')
        plt.title('Total Non Renewable Power Generation')
        # plt.gca().invert_yaxis()

        # Save the plot image
        plot_path = 'static/display_data/images/bar.png'
        plt.savefig(plot_path, format='png')
        plt.close()

        context['plot_path'] = plot_path

        return context


class RenewablesTotalPowerListView(ListView):
    model = RenewableTotalPowerGenerated
    template_name = 'display_data/renewables_total_power_generated.html'
    context_object_name = 'renewables_total_power'

    # TODO: iN THE PLOT.PNG, WE CAN SEE THE GRID IN GIT HUB BUT NO LINES

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        template_name = self.template_name
        context['template_name'] = template_name
        # print("template_name", template_name)

        queryset = RenewableTotalPowerGenerated.objects.all()
        renewable_total_power = pd.DataFrame.from_records(
            queryset.values())

        # Create a bar graph
        plt.figure(figsize=(10, 10))
        plt.bar(renewable_total_power['mode_of_generation'],
                renewable_total_power['contribution_twh'],
                color='skyblue')
        plt.xlabel('Mode of Generation')
        plt.ylabel('Contribution (TWh)')
        plt.title(f'Total Renewable Power Generation')
        plt.xticks(rotation=90)

        # Save the plot image
        plot_path = 'static/display_data/images/bar_renewable_power.png'
        plt.savefig(plot_path, format='png')
        plt.close()

        return context


class RenewablePowerGenerationListView(ListView):
    model = RenewablePowerGenerated
    template_name = 'display_data/renewable_power_generated.html'
    context_object_name = 'renewable_power_generated'
    ordering = ['year']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years = RenewablePowerGenerated.objects.values_list('year', flat=True)
        context['years'] = years

        template_name = self.template_name
        context['template_name'] = template_name
        print("template_name", template_name)

        queryset = RenewablePowerGenerated.objects.all()
        # convert the queryset to a dataframe
        renewable_power = pd.DataFrame.from_records(
            queryset.values())
        # Drop the 'id' column if it exists
        if 'id' in renewable_power.columns:
            renewable_power.drop('id', axis=1, inplace=True)
        # set year as index
        renewable_power.set_index('year', inplace=True)
        # create bar graph
        renewable_power.plot(kind='bar', stacked=True)
        plt.xlabel('Year')
        plt.ylabel('Power Generated (TWh)')
        plt.title(f'Renewable Power Generation by Year (TWh)')

        # save img
        plot_path = 'static/display_data/images/renewable_power_plot.png'
        plt.savefig(plot_path)
        plt.close()

        return context


class RenewablePowerDetailView(DetailView):
    model = RenewablePowerGenerated
    template_name = 'display_data/renewable_power_generated_detail.html'
    context_object_name = 'renewable_power_generated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        renewable_power = self.object  # The object retrieved by the DetailView

        # Prepare data for plotting
        data = {
            'Hydro': renewable_power.hydro,
            'Biofuels': renewable_power.biofuels,
            'Solar': renewable_power.solar,
            'Geo Thermal': renewable_power.geo_thermal,
        }
        renewable_power_df = pd.DataFrame(data, index=['Power Generated (TWh)'])

        # Create a bar graph using the data
        plt.figure(figsize=(10, 10))
        renewable_power_df.plot(kind='bar')
        plt.xlabel('Mode of Generation',
                   rotation=0)
        plt.ylabel('Power Generated (TWh)')
        plt.title(f'Renewable Power Generation for {renewable_power.year}')
        plt.xticks(rotation=90, ha='right')

        # Save the graph as an image file
        plot_path = 'static/display_data/images/renewable_power_plot.png'
        plt.savefig(plot_path)
        plt.close()

        # Pass the graph path and other data to the template
        context['plot_path'] = plot_path

        return context


class RenewablePowerColumnView(TemplateView):
    template_name = ('display_data/renewable_power_column_detail'
                     '.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get column name from url
        column_name = self.kwargs.get('column_name', None)
        # is there a column name?
        if column_name:
            #     get all renewable power generated objects ordered by year
            queryset = RenewablePowerGenerated.objects.all().order_by('year')
            #     convert the queryset to a dataframe
            renewable_power = pd.DataFrame.from_records(
                queryset.values())
            #    get the column data
            column_data = renewable_power[column_name]
            #     add the column data to the context
            context['column_data'] = column_data

            #     create a plot
            plt.figure(figsize=(10, 5))
            plt.plot(renewable_power['year'], column_data)
            plt.xlabel('Year')
            plt.ylabel(f'{column_name}(TWh)')
            plt.title(f'{column_name} by Year (TWh)')
            plt.grid(True)

            # save img
            plot_path = 'static/display_data/images/plot.png'
            plt.savefig(plot_path)
            plt.close()

            context['plot_path'] = plot_path

        return context


class TopTwentyRenewableCountriesListView(ListView):
    model = TopTwentyRenewableCountries
    template_name = 'display_data/top_twenty_renewable_countries.html'
    context_object_name = 'top_twenty_renewable_countries'
    paginate_by = 10
    ordering = ['-total']  # unordered lists return error. Ordered highest
    # to lowest


class TopTwentyRenewableCountriesDetailView(DetailView):
    model = TopTwentyRenewableCountries
    template_name = 'display_data/top_twenty_renewable_countries_detail.html'
    context_object_name = 'top_twenty_renewable_countries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        template_name = self.template_name
        context['template_name'] = template_name
        print("template_name", template_name)

        top_twenty = self.object  # The object retrieved by the DetailView

        values = [top_twenty.hydro, top_twenty.biofuels, top_twenty.solar,
                  top_twenty.geo_thermal, top_twenty.total]
        labels = ['Hydro', 'Biofuels', 'Solar', 'Geo Thermal', 'Total']

        plt.figure(figsize=(10, 10))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel('Renewable energy Sources')
        plt.ylabel(f'Contribution (TWh): {top_twenty.country}')
        plt.title(f'Renewable Power Generation for {top_twenty.country}')

        # Save the graph as an image file
        plot_path = 'static/display_data/images/top_twenty_detail_plot.png'
        plt.savefig(plot_path)
        plt.close()

        # Pass the graph path and other data to the template
        context['plot_path'] = plot_path
        return context


class TopTwentyRenewableCountriesColumnView(TemplateView):
    template_name = (
        'display_data/top_twenty_renewable_countries_column_detail.html')

    # ordering = ['total']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        column_name = self.kwargs.get('column_name', None)

        if column_name:
            queryset = TopTwentyRenewableCountries.objects.all()
            top_twenty = pd.DataFrame.from_records(
                queryset.values())

            column_data = top_twenty[column_name]
            context['column_data'] = column_data

            plt.figure(figsize=(10, 10))
            plt.bar(top_twenty['country'], column_data, color='skyblue')
            plt.xlabel('Country')
            plt.ylabel('Contribution (TWh)')
            plt.title(f'Renewable Power Generation {column_name}')
            plt.xticks(rotation=90)

            # Save the plot image
            plot_path = 'static/display_data/images/top_twenty_column.png'
            plt.savefig(plot_path, format='png')
            plt.close()

            context['plot_path'] = plot_path
        return context


class CountryConsumptionView:
    pass
