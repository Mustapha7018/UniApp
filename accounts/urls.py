from django.urls import path
from .views import *


urlpatterns = [
    path("verify/", CodeVerificationView.as_view(), name="verify"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", PasswordResetConfirmView.as_view(), name="reset-password"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete-account/", AccountDeleteView.as_view(), name="delete-account"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("verify-email/<int:user_id>/", VerifyEmailView.as_view(), name="verify-email"),
    path("favorites/", FavoritesView.as_view(), name="favorites"),
]
