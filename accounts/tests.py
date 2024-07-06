from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CodeEmail, CustomUser, ResetPasswordCode
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from wagtail.models import Page
from blogs.models import BlogIndexPage, BlogPage
from django.utils import timezone
from .utils.functions import generate_activation_code

CustomUser = get_user_model()


''' TEST REGISTER, VERIFY, LOGIN '''
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  
        self.verify_url = reverse('verify')  
        self.login_url = reverse('login')

        Page.objects.filter(slug='home').delete()

        root = Page.objects.get(id=1)
        home_page = Page(title="Home", slug="home")
        root.add_child(instance=home_page)
        home_page.save()

        # Create a BlogIndexPage and some BlogPages
        self.blog_index = BlogIndexPage(title="Blog", slug="blog")
        home_page.add_child(instance=self.blog_index)
        self.blog_index.save()

        for i in range(3):
            blog_page = BlogPage(
                title=f"Blog Post {i+1}",
                date=timezone.now(),
                slug=f"blog-post-{i+1}",
                body="This is a test blog post.",
                intro="This is the intro for the blog post."
            )
            self.blog_index.add_child(instance=blog_page)
            blog_page.save()


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
        self.reset_password_url = reverse('reset-password')

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
        self.assertTrue(ResetPasswordCode.objects.filter(user=self.user).exists())

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
        reset_code = ResetPasswordCode.objects.create(user=self.user, code=generate_activation_code())
        reset_data = {
            'verification_code': reset_code.code,
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
        self.assertFalse(ResetPasswordCode.objects.filter(user=self.user).exists())

    def test_password_reset_confirm_view_post_passwords_do_not_match(self):
        reset_code = ResetPasswordCode.objects.create(user=self.user, code=generate_activation_code())
        reset_data = {
            'verification_code': reset_code.code,
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
        reset_code = ResetPasswordCode.objects.create(user=self.user, code=generate_activation_code())
        reset_data = {
            'verification_code': reset_code.code,
            'password1': 'short',
            'password2': 'short'
        }
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reset_password_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Password must be at least 8 characters.')

    def test_password_reset_confirm_view_post_invalid_code(self):
        reset_data = {
            'verification_code': 'invalid_code',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reset_password_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid verification code.')

    def test_password_reset_confirm_view_post_missing_fields(self):
        reset_data = {}  # Empty data
        response = self.client.post(self.reset_password_url, reset_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reset_password_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please fill in all fields.')