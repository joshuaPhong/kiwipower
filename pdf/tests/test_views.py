from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch, Mock
from io import StringIO


class PdfViewTest(TestCase):
    """
    Test the pdf view
    """

    def test_response_status_code(self):
        """
        Test that the response status code is 200 for each url
        :return: None
        """
        urls = ['pdf_one', 'pdf_two', 'pdf_three', 'pdf_four', 'pdf_five',
                'pdf_six']
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code,
                             200)

    def test_response_content_type(self):
        """
        Test that the response content type is pdf
        :return: None
        """
        urls = ['pdf_one', 'pdf_two', 'pdf_three', 'pdf_four', 'pdf_five',
                'pdf_six']
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response['Content-Type'],
                             'application/pdf')

    def test_response_content_disposition(self):
        """
        Test that the response content disposition is filename="table.pdf"
        :param self: the test class
        :return: None
        """

        urls = ['pdf_one', 'pdf_two', 'pdf_three', 'pdf_four', 'pdf_five',
                'pdf_six']
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response['Content-Disposition'],
                             'filename="table.pdf"')

    from unittest.mock import Mock, patch

    def test_pisa_error_handling(self):
        mock_pisa = Mock()
        mock_pisa.err = True  # Add 'err' attribute to the mock object

        with patch('pdf.views.pisa.CreatePDF', return_value=mock_pisa):
            response = self.client.get(reverse('pdf_one'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('We had some errors', response.content.decode())
