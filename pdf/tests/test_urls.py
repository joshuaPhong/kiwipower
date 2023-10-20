from django.urls import reverse, resolve
from unittest import TestCase

from django.urls import reverse

from pdf.views import pdf_two


class UrlsTest(TestCase):
    """
    Test the URLS for the pdf app
    """

    def test_pdf_one_url(self):
        """
        Test pdf_one url
        :return: pass, error, or fail
        """
        url = reverse('pdf_one')
        self.assertEqual(resolve(url).func,
                         pdf_two)

    def test_pdf_two_url(self):
        """
        Test pdf_two url
        :return: pass, error, or fail
        """
        url = reverse('pdf_two')
        self.assertEqual(resolve(url).func,
                         pdf_two)

    def test_pdf_three_url(self):
        """
        Test pdf_three url
        :return: pass, error, or fail
        """
        url = reverse('pdf_three')
        self.assertEqual(resolve(url).func,
                         pdf_two)

    def test_pdf_four_url(self):
        """
        Test pdf_four url
        :return: pass, error, or fail
        """
        url = reverse('pdf_four')
        self.assertEqual(resolve(url).func,
                         pdf_two)

    def test_pdf_five_url(self):
        """
        Test pdf_five url
        :return: pass, error, or fail
        """
        url = reverse('pdf_five')
        self.assertEqual(resolve(url).func,
                         pdf_two)

    def test_pdf_six_url(self):
        """
        Test pdf_six url
        :return: pass, error, or fail
        """
        url = reverse('pdf_six')
        self.assertEqual(resolve(url).func,
                         pdf_two)
