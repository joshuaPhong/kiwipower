# https://mitesh.dev/blog/django-set-path-global-static-files
# https://stackoverflow.com/questions/49442501/static-files-not-found-error
# -in-django


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from display_data.models import (ContinentConsumption, CountryConsumption,
                                 RenewablePowerGenerated,
                                 NonRenewablesTotalPowerGenerated,
                                 TopTwentyRenewableCountries,
                                 RenewableTotalPowerGenerated)
import os
from django.conf import settings


# fixme: I couldn't get this to work. Some url thing I think. I could pass
#  the context to the template and see it in the browser, and debug mode.
#  Always got a no reverse match error.
# def generate_pdf_dynamic_nav(request, template_name):
#     if template_name == 'display_data/country_energy_consumption.html':
#         table_data = CountryConsumption.objects.all()
#         context = {
#             'country_consumption': table_data,
#         }
#     elif template_name == 'display_data/continent_energy_consumption.html':
#         table_data = ContinentConsumption.objects.all()
#         years = ContinentConsumption.objects.values_list('year',
#                                                          flat=True).distinct()
#         context = {
#             'continent_consumption': table_data,
#             'years': years,
#         }
#     elif template_name == ('display_data/non_renewables_total_power_generated'
#                            '.html'):
#         table_data = NonRenewablesTotalPowerGenerated.objects.all()
#
#         context = {
#             'non_renewables_total_power': table_data,
#         }
#     elif template_name == 'display_data/renewables_power_generated.html':
#         table_data = RenewablePowerGenerated.objects.all()
#         context = {
#             'renewable_power_generated': table_data,
#         }
#     elif template_name == 'display_data/renewables_total_power_generated
#     .html':
#         table_data = RenewableTotalPowerGenerated.objects.all()
#         context = {
#             'renewable_total_power_generated': table_data,
#         }
#     elif template_name == 'display_data/top_twenty_renewable_countries.html':
#         table_data = TopTwentyRenewableCountries.objects.all()
#         context = {
#             'top_twenty_renewable_countries': table_data,
#         }
#     else:
#         print('no template name')
#
#     template_path = f'{template_name}'
#
#     template = get_template(template_path)
#
#     html = template.render(context)
#
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="table.pdf"'
#
#     pisa_status = pisa.CreatePDF(
#         html, dest=response, link_callback=fetch_resources,
#         page_size='A4 landscape')
#
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#
#     return response
#
#
# def pdf_one(request):
#     """
#     Function to generate a pdf from a template.
#     This works but only does a single template
#     :param request:
#     :return: a response object
#     """
#     template_path = 'display_data/country_energy_consumption.html'
#     template = get_template(template_path)
#
#     table_data = CountryConsumption.objects.all()
#     context = {
#         'country_consumption': table_data,
#     }
#
#     html = template.render(context)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="table.pdf"'
#
#     pisa_status = pisa.CreatePDF(
#         html, dest=response, link_callback=fetch_resources)
#
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#
#     return response


# fixme: we could take the template name from the url as context and pass it
#  to the pdf view. As a parameter. We could dry our code a bit.
def pdf_two(request):
    """
    Function to generate a pdf from a template.
    This works on all the list views and their graphs.
    :param request:
    :return: response object
    """
    # get the url name
    url_name = request.resolver_match.url_name
    # test the name of the url
    if url_name == 'pdf_one':
        template_path = f'display_data/country_energy_consumption.html'
        template = get_template(template_path)

        table_data = CountryConsumption.objects.all()
        context = {
            'country_consumption': table_data,
        }
    elif url_name == 'pdf_two':
        template_path = f'display_data/continent_energy_consumption.html'
        template = get_template(template_path)

        table_data = ContinentConsumption.objects.all()
        context = {
            'continent_consumption': table_data,
        }
    elif url_name == 'pdf_three':
        template_path = 'display_data/non_renewables_total_power_generated.html'
        template = get_template(template_path)

        table_data = NonRenewablesTotalPowerGenerated.objects.all()
        context = {
            'non_renewables_total_power': table_data,
        }
    elif url_name == 'pdf_four':

        template_path = f'display_data/renewable_power_generated.html'
        template = get_template(template_path)

        table_data = RenewablePowerGenerated.objects.all()
        context = {
            'renewable_power_generated': table_data,
        }
    elif url_name == 'pdf_five':
        template_path = f'display_data/renewables_total_power_generated.html'
        template = get_template(template_path)

        table_data = RenewableTotalPowerGenerated.objects.all()
        context = {
            'renewables_total_power': table_data,
        }
    elif url_name == 'pdf_six':
        template_path = f'display_data/top_twenty_renewable_countries.html'
        template = get_template(template_path)

        table_data = TopTwentyRenewableCountries.objects.all()
        context = {
            'top_twenty_renewable_countries': table_data,
        }
    else:
        print('no url name')

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="table.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=fetch_resources)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def fetch_resources(uri, rel):
    """
    Function to fetch resources (like CSS) while generating the PDF.
    I did not use this, because it would not fetch my graphs from static.
    Instead, I configured the static files in settings.py and ran collect-static
    :param uri:
    :param rel:
    :return: a path to static and media files
    """
    if uri.startswith('/static/'):
        path = os.path.join(settings.STATIC_ROOT, uri.replace('/static/', ''))
    elif uri.startswith('/media/'):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace('/media/', ''))
    else:
        path = None
    return path
