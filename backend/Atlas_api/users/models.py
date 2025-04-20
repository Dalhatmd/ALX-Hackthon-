from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Core user model for workspace booking MVP"""

    class UserType(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")  # Can create bookings for team
        GENERAL = "GENERAL", _("General")  # Solo booker
        EMPLOYEE = "EMPLOYEE", _("Employee")
        OWNER = "OWNER", _("Owner")  # Workspace owner

    email = models.EmailField("email address", unique=True)
    phone = models.CharField(max_length=20, blank=True)  # Only essential contact field
    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default=UserType.GENERAL
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def is_owner(self):
        return self.user_type == self.UserType.OWNER

    def is_admin(self):
        return self.user_type == self.UserType.ADMIN
