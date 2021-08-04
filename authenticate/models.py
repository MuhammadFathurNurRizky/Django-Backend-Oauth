from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must be sign as is_staff = True"
            )

        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be sign as is_superuser = True"
            )

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user  = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

AUTH_PROVIDERS = {"facebook": "facebook", "google": "google", "twitter": "twitter", "email": "email"}

class NewUser(AbstractBaseUser, PermissionsMixin):
    email         = models.EmailField(_("email address"), unique=True)
    user_name     = models.CharField(max_length=150, unique=True)
    start_date    = models.DateTimeField(default=timezone.now)
    updated_at    = models.DateTimeField(auto_now=True)
    is_verified   = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    auth_provider = models.CharField(max_length=255, blank=True, null=False, default=AUTH_PROVIDERS.get("email"))

    objects    = CustomAccountManager()

    REQUIRED_FIELDS = ["user_name"]
    USERNAME_FIELD  = "email"

    def __str__(self):
        return "name: %s, date: %s" % (self.user_name, self.start_date)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
