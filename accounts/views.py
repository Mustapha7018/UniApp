import re
import logging
from django.http.response import HttpResponseRedirect
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .forms import CustomUserChangeForm
from .models import CustomUser, CodeEmail, ResetPasswordCode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import UpdateView, DeleteView
from .utils.functions import generate_activation_code, is_expired
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

logger = logging.getLogger(__name__)


class AdminOnlyView(LoginRequiredMixin, UserPassesTestMixin):
    template_name = "admin_page.html"

    def test_func(self) -> bool:
        return self.request.user.is_superuser

    def handle_no_permission(self) -> HttpResponseRedirect:
        return super().handle_no_permission()


""" REGISTER USER """


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
            redirect_url = request.META.get("HTTP_REFERER", reverse("register"))
            return redirect(redirect_url)

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            redirect_url = request.META.get("HTTP_REFERER", reverse("register"))
            return redirect(redirect_url)

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            messages.error(request, "Invalid email address format.")
            redirect_url = request.META.get("HTTP_REFERER", reverse("register"))
            return redirect(redirect_url)

        if CustomUser.objects.filter(email=email_address).exists():
            messages.error(request, "Email already exists.")
            redirect_url = request.META.get("HTTP_REFERER", reverse("register"))
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
                message.attach_alternative(html_message, "text/html")
                message.send()
                messages.success(request, "Email verification code sent to email.")
                return redirect("verify")
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                messages.error(request, f"Error sending email: {e}, please try again.")
                redirect_url = request.META.get("HTTP_REFERER", reverse("register"))
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
                code=generated_code,
            )
            code_user.save()
            message = EmailMultiAlternatives(
                subject="Email Verification Code",
                body=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email_address],
            )
            message.attach_alternative(html_message, "text/html")
            message.send()
            messages.success(request, "Email verification code sent to email.")
            return redirect("verify")
        except Exception as e:
            logger.error(f"Error creating CodeEmail or sending email: {e}")
            messages.error(
                request,
                f"Error creating CodeEmail or sending email: {e}, please try again.",
            )
            redirect_url = request.META.get("HTTP_REFERER", reverse("register"))
            return redirect(redirect_url)

        return render(request, self.template_name)


""" VIEW FOR CODE VERIFICATION """


class CodeVerificationView(View):
    template_name = "pages/code_verification.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        try:
            code_email = CodeEmail.objects.get(code=code)
            user = CustomUser.objects.create_user(
                email=code_email.email,
                username=code_email.email,
                password=code_email.password,
                fullname=code_email.fullname,
            )
            user.save()
            code_email.delete()
            messages.success(
                request, "Email verified and account created. Please log in."
            )
            return redirect("login")
        except CodeEmail.DoesNotExist:
            messages.error(request, "Invalid code. Please try again.")
            return redirect("verify")
        return render(request, self.template_name, {"form": form})


""" VIEW TO LOG IN USERS """


class CustomLoginView(View):
    template_name = "pages/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            fullname = user.fullname or "User"
            first_name = fullname.split()[0] if " " in fullname else fullname
            messages.success(request, f"Welcome back, {first_name}!")

            next_url = request.POST.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                if "reset-password" not in next_url:
                    return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect(reverse("login"))


""" VIEW TO LOG OUT USERS """


class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("login")


""" VIEW TO RESET PASSWORD """


class ForgotPasswordView(View):
    template_name = "pages/forgot_password.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            generated_code = generate_activation_code()

            ResetPasswordCode.objects.create(user=user, code=generated_code)

            # Prepare email content
            context = {
                "generated_code": generated_code,
                "user": user,
            }
            html_message = render_to_string("pages/verify.html", context)
            plain_message = strip_tags(html_message)

            # Send email with verification code
            subject = "Password Reset Verification Code"
            try:
                message = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                )
                message.attach_alternative(html_message, "text/html")
                message.send()
                messages.success(request, "Verification code sent to your email.")
                return redirect("reset-password")
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                messages.error(request, f"Error sending email: {e}, please try again.")
                return redirect("forgot-password")
        except CustomUser.DoesNotExist:
            messages.error(request, "Email address not found.")
            return redirect("forgot-password")


""" VIEW TO CONFIRM PASSWORD RESET """


class PasswordResetConfirmView(View):
    template_name = "pages/reset_password.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        verification_code = request.POST.get("verification_code")
        new_password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        if not all([verification_code, new_password, confirm_password]):
            messages.error(request, "Please fill in all fields.")
            return redirect("reset-password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset-password")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("reset-password")

        try:
            reset_code = ResetPasswordCode.objects.get(code=verification_code)
            user = reset_code.user

            if is_expired(reset_code.created_at):
                messages.error(request, "The verification code has expired.")
                return redirect("forgot-password")

            user.set_password(new_password)
            user.save()
            reset_code.delete()
            messages.success(request, "Your password has been reset. Please log in.")
            return redirect("login")
        except ResetPasswordCode.DoesNotExist:
            messages.error(request, "Invalid verification code.")
            return redirect("reset-password")


""" VIEW TO UPDATE PROFILE """


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "pages/profile.html"
    success_url = reverse_lazy("profile-update")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        new_email = form.cleaned_data["email"]

        if user.email != new_email:
            user.new_email = new_email
            user.email_verified = False
            user.save()
            verification_link = self.request.build_absolute_uri(
                reverse("verify-email", args=[user.id])
            )
            context = {
                "verification_link": verification_link,
            }
            html_message = render_to_string("pages/email_verification.html", context)
            plain_message = strip_tags(html_message)

            try:
                message = EmailMultiAlternatives(
                    subject="Verify your new email address",
                    body=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[new_email],
                )
                message.attach_alternative(html_message, "text/html")
                message.send()
                messages.info(
                    self.request, "Verification email sent to your new email address"
                )
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                messages.error(
                    self.request, f"Error sending email: {e}, please try again"
                )
                return super().form_invalid(form)
        else:
            user.save()

        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)


""" VERIFY EMAIL """


class VerifyEmailView(View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        if user.new_email:
            user.email = user.new_email
            user.new_email = None
            user.email_verified = True
            user.save()
            messages.success(request, "Email address updated successfully.")
        else:
            messages.error(request, "Email verification failed.")
        return redirect("profile-update")


""" VIEW TO DISPLAY FAVORITES """


class FavoritesView(LoginRequiredMixin, View):
    template_name = "pages/favorites.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


""" VIEW TO DELETE ACCOUNT """


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "pages/account_confirm_delete.html"
    success_url = reverse_lazy("home")  # Redirect to the home page after deletion

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your account has been deleted.")
        return super().delete(request, *args, **kwargs)
