from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CodeEmail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

CustomUser = get_user_model()


''' TEST REGISTER, VERIFY, LOGIN '''
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


''' TEST LOGOUT, FORGOT PASSWORD, RESET PASSWORD '''
class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='test@example.com', password='password123', fullname='Test User'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.forgot_password_url = reverse('forgot-password')
        self.reset_password_url = reverse('reset-password', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': default_token_generator.make_token(self.user)
        })

    def test_logout_view(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_forgot_password_view_get(self):
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/forgot_password.html')

    def test_forgot_password_view_post_user_exists(self):
        response = self.client.post(self.forgot_password_url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reset_password_url)

    def test_forgot_password_view_post_user_does_not_exist(self):
        response = self.client.post(self.forgot_password_url, {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.forgot_password_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Email address not found.')

    def test_password_reset_confirm_view_get(self):
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/reset_password.html')

    def test_password_reset_confirm_view_post_success(self):
        reset_data = {
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your password has been reset. Please log in.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_password_reset_confirm_view_post_passwords_do_not_match(self):
        reset_data = {
            'password1': 'newpassword123',
            'password2': 'differentpassword123'
        }
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reset_password_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Passwords do not match.')

    def test_password_reset_confirm_view_post_password_too_short(self):
        reset_data = {
            'password1': 'short',
            'password2': 'short'
        }
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reset_password_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Password must be at least 8 characters.')

    def test_password_reset_confirm_view_post_invalid_link(self):
        invalid_reset_url = reverse('reset-password', kwargs={
            'uidb64': 'invalid',
            'token': 'invalid-token'
        })
        reset_data = {
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(invalid_reset_url, reset_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.forgot_password_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The reset link is invalid or has expired.')
