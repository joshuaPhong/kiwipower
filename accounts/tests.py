# source https://djangoforbeginners.com/pages-app/
from django.test import TestCase
from accounts.models import CustomUser
from django.urls import reverse

class SignUpTests(TestCase):
    def setUp(self):
        # Create user data for testing registration
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        # Create a user for other tests to use
        self.user = CustomUser.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password1']
        )

    # def test_url_exists_at_correct_location(self):
    #     response = self.client.get(reverse('signup'))
    #     self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        response = self.client.post(reverse('signup'), self.user_data, follow=True)

        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, reverse('login'))

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    # def test_correct_template_used(self):
    #      self.assertTemplateUsed(response, 'registration/signup.html')
