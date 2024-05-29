from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CodeEmail

CustomUser = get_user_model()

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  
        self.verify_url = reverse('verify')  
        self.login_url = reverse('login')  

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/register.html')

    def test_register_view_post_invalid_password(self):
        data = {
            'fullname': 'Test User',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password124'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.register_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Passwords do not match.")

    def test_register_view_post_invalid_email(self):
        data = {
            'fullname': 'Test User',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.register_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid email address format.")

    def test_register_view_post_email_exists(self):
        CustomUser.objects.create_user(
            email='test@example.com', password='password123', fullname='Test User'
        )
        data = {
            'fullname': 'Test User',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.register_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email already exists.")

    def test_register_view_post_success(self):
        data = {
            'fullname': 'Test User',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.verify_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email verification code sent to email.")
        self.assertTrue(CodeEmail.objects.filter(email='test@example.com').exists())

    def test_code_verification_view_get(self):
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/code_verification.html')

    def test_code_verification_view_post_invalid_code(self):
        data = {'code': 123456}
        response = self.client.post(self.verify_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.verify_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid code. Please try again.")

    def test_custom_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.html')

    def test_custom_login_view_post_invalid_credentials(self):
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid email or password. Please try again.")

    def test_custom_login_view_post_success(self):
        user = CustomUser.objects.create_user(
            email='test@example.com', password='password123', fullname='Test User'
        )
        data = {'email': 'test@example.com', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("Welcome back,", str(messages[0]))
