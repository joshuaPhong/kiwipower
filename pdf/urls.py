from django.urls import path

from .views import PdfView

urlpatterns = [

    path('signup/', PdfView.as_view(), name='signup'),
]
