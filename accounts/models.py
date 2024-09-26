from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from university.models import University


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email Address field must be set")
        email_address = self.normalize_email(email)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    new_email = models.EmailField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=False, null=False)
    course = models.CharField(max_length=255, blank=True, null=True)
    preferred_course = models.CharField(max_length=255, blank=True, null=True)
    aggregate = models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", default="images/profile_img.png"
    )
    favorites = models.ManyToManyField(University, related_name="favorited_by", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CodeEmail(models.Model):
    fullname = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    password = models.CharField(blank=False, null=False, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.email


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)