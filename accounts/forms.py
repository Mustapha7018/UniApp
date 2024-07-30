from django import forms
from .models import CustomUser
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("fullname", "email")


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "fullname",
            "email",
            "course",
            "location",
            "preferred_course",
            "aggregate",
            "profile_picture",
        ]
        widgets = {
            "profile_picture": forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_picture"].required = False

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and CustomUser.objects.filter(email=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("A user with that email already exists.")
        return email
