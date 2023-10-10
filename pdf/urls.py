from django.urls import path

from . import views

urlpatterns = [

    path('generate_pdf/', views.generate_pdf, name='pdf'),
]
