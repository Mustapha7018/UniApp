from django import forms
from .models import CustomUser
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm
)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('fullname', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('fullname', 'email', 'academic_background', 'location')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class CodeVerificationForm(forms.Form):
    code = forms.IntegerField(label='Verification Code', min_value=100000, max_value=999999)

