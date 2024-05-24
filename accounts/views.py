from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from .models import CustomUser, CodeEmail
from .forms import CodeVerificationForm
from .utils.functions import generate_activation_code
import re

from django.http import HttpResponse

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
            return redirect(request.META.get("HTTP_REFERER"))
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect(request.META.get("HTTP_REFERER"))
        
        # Validate email address format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            messages.error(request, "Invalid email address format.")
            return redirect(request.META.get("HTTP_REFERER"))

        if CustomUser.objects.filter(email=email_address).exists():
            messages.error(request, "Email already exists.")
            return redirect(request.META.get("HTTP_REFERER"))

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
                messages.error(request, f"Error sending email: {e}, please try again.")
                return redirect(request.META.get("HTTP_REFERER"))
        
        # Generate Verification Code
        generated_code = generate_activation_code()
        context = {
            "generated_code": generated_code,
        }
        html_message = render_to_string("pages/verify.html", context)
        plain_message = strip_tags(html_message)

        code_user = CodeEmail.objects.create(email=email_address, password=password, fullname=fullname, code=generated_code)
        code_user.save()

        # Send Email with verification Code to User Email 
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
            messages.error(request, f"Error sending email: {e}, please try again.")
            return redirect(request.META.get("HTTP_REFERER"))

        return render(request, self.template_name)


class CodeVerificationView(View):
    template_name = "pages/code_verification.html"

    def get(self, request, *args, **kwargs):
        form = CodeVerificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                code_email = CodeEmail.objects.get(code=code)
                user = CustomUser.objects.create_user(
                    email=code_email.email,
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
        else:
            return render(request, self.template_name, {'form': form})


def loginView(request):
    return render(request, 'pages/login.html')