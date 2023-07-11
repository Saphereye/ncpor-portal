from typing import Any
from django.contrib.auth.models import (
    AbstractUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email not provided")
        if not password:
            raise ValueError("Password not provided")

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Details(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, default="", null=False)
    last_name = models.CharField(max_length=20, default="", null=False)
    mobile = PhoneNumberField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length = 1,choices = GENDER_CHOICES, null=False)
    qualification = models.CharField(max_length=20, null=False)
    designation = models.CharField(max_length=20, null=False)
    institute = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=20, null=False)
    is_pi = models.BooleanField(default=True)
    is_verifier = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)

