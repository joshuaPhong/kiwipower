from django.urls import path, include

from . import views

urlpatterns = [
    # fixme: i couldn't get this to work, ii got the no reverse match error
    # path('generate_pdf/<str:template_name>/', views.generate_pdf, name='pdf'),
    # fixme: I could pass the template name as context and pass it to the pdf
    #  view.
    path('pdf_one/', views.pdf_two, name='pdf_one'),
    path('pdf_two/', views.pdf_two, name='pdf_two'),
    path('pdf_three/', views.pdf_two, name='pdf_three'),
    path('pdf_four/', views.pdf_two, name='pdf_four'),
    path('pdf_five/', views.pdf_two, name='pdf_five'),
    path('pdf_six/', views.pdf_two, name='pdf_six'),

]
