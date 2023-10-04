from django.views.generic import ListView, DetailView, TemplateView
from .models import ContinentConsumption, CountryConsumption, \
    NonRenewablesTotalPowerGenerated
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years = ContinentConsumption.objects.values_list('year', flat=True)
        context['years'] = years
        return context


class ContinentConsumptionDetailView(DetailView):
    model = ContinentConsumption
    template_name = 'display_data/continent_energy_consumption_detail.html'
    context_object_name = 'continent_consumption'


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

            column_data = continent_consumption[column_name]
            context['column_data'] = column_data

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


class CountryConsumptionView(TemplateView):
    template_name = 'display_data/country_energy_consumption_combined.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all CountryConsumption objects ordered by year
        queryset = CountryConsumption.objects.all().order_by('year')

        # Convert the queryset to a DataFrame
        df = pd.DataFrame.from_records(queryset.values())

        # Calculate the minimum and maximum for each row
        df['min'] = df.min(axis=1)
        df['max'] = df.max(axis=1)

        # Add the DataFrame to the context (convert to HTML for display in
        # the template)
        context['df'] = df.to_html(classes='table table-bordered')

        # Create a plot for each country
        for column in df.columns:
            if column not in ['id', 'year', 'min', 'max']:
                plt.figure(figsize=(10, 5))
                plt.plot(df['year'], df[column])
                plt.xlabel('Year')
                plt.ylabel(f'{column} (TWh)')
                plt.title(f'{column} by Year (TWh)')
                plt.grid(True)

                # Save the plot to a file
                plot_path = f'static/display_data/images/{column}_plot.png'
                plt.savefig(plot_path)
                plt.close()

                # Add the plot path to the context
                context[f'{column}_plot_path'] = plot_path

        return context


class CountryConsumptionListView(ListView):
    model = CountryConsumption
    template_name = 'display_data/country_energy_consumption.html'
    context_object_name = 'country_consumption'
    ordering = ['year']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years = CountryConsumption.objects.values_list('year', flat=True)
        context['years'] = years
        return context


class CountryConsumptionDetailView(DetailView):
    model = CountryConsumption
    template_name = 'display_data/country_energy_consumption_detail.html'
    context_object_name = 'country_consumption'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('year')

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
        column_name = self.kwargs.get('column_name', None)

        if column_name:
            queryset = NonRenewablesTotalPowerGenerated.objects.all()
            non_renewable_power = pd.DataFrame.from_records(
                queryset.values())

            column_data = non_renewable_power[column_name]
            context['column_data'] = column_data

            # Create a bar graph
            plt.figure(figsize=(10, 6))
            plt.barh(non_renewable_power['mode_of_generation'], column_data,
                     color='skyblue')
            plt.xlabel('Contribution (TWh)')
            plt.title(f'{column_name} by Mode of Generation')
            plt.gca().invert_yaxis()  # Invert the y-axis for better readability

            # Annotate the bars with values
            for i, v in enumerate(column_data):
                plt.text(v + 100, i, str(v), color='black', va='center',
                         fontsize=12, fontweight='bold')

            # Save the plot image
            plot_path = 'static/display_data/images/bar.png'
            plt.savefig(plot_path, format='png')
            plt.close()

            context['plot_path'] = plot_path

        return context


class CountryConsumptionCombinedView:
    pass
