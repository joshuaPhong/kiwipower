from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here
class HomePageView(TemplateView):
    '''
    This class is used to render the home page
    '''
    template_name = 'pages/home.html'
