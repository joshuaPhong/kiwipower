from django.views.generic import ListView, DetailView, TemplateView
from .models import ContinentConsumption
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
