from django.urls import path
from .views import CodeVerificationView, RegisterView, CustomLoginView



urlpatterns = [
    path('verify/', CodeVerificationView.as_view(), name='verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]