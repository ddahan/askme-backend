from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from model_utils.models import TimeStampedModel


class CustomUserManager(BaseUserManager):
    """
    Custom User Manager is required when redefining User class
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        """

        email = CustomUserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False,
                          is_active=True,
                          is_superuser=False,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        """

        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    """
    Redefined custom Django User class.
    AbstractBaseUser provides the core implementation of a User model.
    """

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=1024, blank=True)
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # used as the unique identifier
    REQUIRED_FIELDS = []  # a list of the field names that will be prompted with createsuperuser

    def get_full_name(self):
        """ Returns the first_name plus the last_name, with a space in between """

        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Returns the short name for the user """

        return self.first_name

    def __str__(self):
        return self.get_full_name()


class Customer(TimeStampedModel):
    """
    Customer
    """

    user = models.ForeignKey(User, help_text=_("utilisateur"))

    def __str__(self):
        return self.user.get_full_name()