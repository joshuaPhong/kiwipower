from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

import os
from django.conf import settings

from display_data.models import ContinentConsumption, CountryConsumption


def generate_pdf(request):
    # Your queryset or context data for the table goes here
    table_data = CountryConsumption.objects.all()
    years = ContinentConsumption.objects.values_list('year',
                                                     flat=True).distinct()

    context = {
        'country_consumption': table_data,
    }

    template_path = 'display_data/country_energy_consumption.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="table.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=fetch_resources,
        page_size='A4 landscape')

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def fetch_resources(uri, rel):
    # Function to fetch resources (like CSS) while generating the PDF
    if uri.startswith('/static/'):
        path = os.path.join(settings.STATIC_ROOT, uri.replace('/static/', ''))
    elif uri.startswith('/media/'):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace('/media/', ''))
    else:
        path = None
    return path
