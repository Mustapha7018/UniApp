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
from django.contrib.auth import authenticate, login
from .utils.functions import (
    generate_activation_code,
    is_expired
)

logger = logging.getLogger(__name__)

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
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect(reverse('login'))



            


        