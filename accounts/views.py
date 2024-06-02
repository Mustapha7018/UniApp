import re
import logging
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .models import CustomUser, CodeEmail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.tokens import default_token_generator
from .utils.functions import (
    generate_activation_code,
    is_expired
)
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView
)

logger = logging.getLogger(__name__)

''' REGISTER USER '''
class RegisterView(View):
    template_name = "pages/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        fullname = request.POST.get("fullname")
        email_address = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            redirect_url = request.META.get("HTTP_REFERER", reverse('register'))
            return redirect(redirect_url)

        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            redirect_url = request.META.get("HTTP_REFERER", reverse('register'))
            return redirect(redirect_url)

        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            messages.error(request, "Invalid email address format.")
            redirect_url = request.META.get("HTTP_REFERER", reverse('register'))
            return redirect(redirect_url)


        if CustomUser.objects.filter(email=email_address).exists():
            messages.error(request, "Email already exists.")
            redirect_url = request.META.get("HTTP_REFERER", reverse('register'))
            return redirect(redirect_url)


        if CodeEmail.objects.filter(email=email_address).exists():
            code_user = CodeEmail.objects.get(email=email_address)
            generated_code = generate_activation_code()
            code_user.code = generated_code
            code_user.save()
            context = {
                "generated_code": generated_code,
            }
            html_message = render_to_string("pages/verify.html", context)
            plain_message = strip_tags(html_message)

            try:
                message = EmailMultiAlternatives(
                    subject="Email Verification Code",
                    body=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email_address],

                )
                message.attach_alternative(html_message, 'text/html')
                message.send()
                messages.success(request, "Email verification code sent to email.")
                return redirect("verify")
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                messages.error(request, f"Error sending email: {e}, please try again.")
                redirect_url = request.META.get("HTTP_REFERER", reverse('register'))
            return redirect(redirect_url)

        
        generated_code = generate_activation_code()
        context = {
            "generated_code": generated_code,
        }
        html_message = render_to_string("pages/verify.html", context)
        plain_message = strip_tags(html_message)

        try:
            code_user = CodeEmail.objects.create(
                email=email_address, 
                password=password, 
                fullname=fullname, 
                code=generated_code
            )
            code_user.save()
            message = EmailMultiAlternatives(
                subject="Email Verification Code",
                body=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email_address],
            )
            message.attach_alternative(html_message, 'text/html')
            message.send()
            messages.success(request, "Email verification code sent to email.")
            return redirect("verify")
        except Exception as e:
            logger.error(f"Error creating CodeEmail or sending email: {e}")
            messages.error(request, f"Error creating CodeEmail or sending email: {e}, please try again.")
            redirect_url = request.META.get("HTTP_REFERER", reverse('register'))
            return redirect(redirect_url)


        return render(request, self.template_name)


''' VIEW FOR CODE VERIFICATION '''
class CodeVerificationView(View):
    template_name = "pages/code_verification.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        try:
            code_email = CodeEmail.objects.get(code=code)
            user = CustomUser.objects.create_user(
                email=code_email.email,
                username=code_email.email,
                password=code_email.password,
                fullname=code_email.fullname
            )
            user.save()
            code_email.delete()
            messages.success(request, "Email verified and account created. Please log in.")
            return redirect('login')
        except CodeEmail.DoesNotExist:
            messages.error(request, "Invalid code. Please try again.")
            return redirect('verify')
        return render(request, self.template_name, {'form': form})


''' VIEW TO LOG IN USERS '''
class CustomLoginView(View):
    template_name = 'pages/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            fullname = user.fullname or "User"
            first_name = fullname.split()[0] if ' ' in fullname else fullname
            messages.success(request, f"Welcome back, {first_name}!")

            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                if 'reset-password' not in next_url:
                    return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect(reverse('login'))



''' VIEW TO LOG OUT USERS '''
class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


''' VIEW TO RESET PASSWORD '''
class ForgotPasswordView(View):
    template_name = "pages/forgot_password.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = reverse_lazy('reset-password', kwargs={'uidb64': uid, 'token': token})
            
            return redirect(reset_url)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email address not found.')
            return redirect('forgot-password')


''' VIEW TO CONFIRM PASSWORD RESET '''
class PasswordResetConfirmView(View):
    template_name = "pages/reset_password.html"

    def get(self, request, uidb64, token, *args, **kwargs):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, self.template_name, context)

    def post(self, request, uidb64, token, *args, **kwargs):
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if new_password is None or confirm_password is None:
            messages.error(request, "Please fill in both password fields.")
            return redirect('reset-password', uidb64=uidb64, token=token)

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset-password', uidb64=uidb64, token=token)

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect('reset-password', uidb64=uidb64, token=token)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset. Please log in.")
                return redirect('login')
            else:
                messages.error(request, "The reset link is invalid or has expired.")
                return redirect('forgot-password')
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            messages.error(request, "The reset link is invalid or has expired.")
            return redirect('forgot-password')


''' VIEW TO DISPLAY USER PROFILE '''
class ProfileView(LoginRequiredMixin, View):
    template_name = 'pages/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


''' VIEW TO DISPLAY FAVORITES '''
class FavoritesView(LoginRequiredMixin, View):
    template_name = 'pages/favorites.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)