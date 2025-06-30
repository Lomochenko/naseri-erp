from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a User with the given phone number and password."""
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a regular User with the given phone number and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone number and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(phone_number, password, **extra_fields)

    def get_queryset(self):
        # Exclude soft-deleted users by default
        return super().get_queryset().filter(is_deleted=False)

class User(AbstractUser):
    """Custom User model with phone number as the unique identifier."""

    username = None
    phone_number = models.CharField(_('phone number'), max_length=15, unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), blank=True)

    # User roles
    is_manager = models.BooleanField(_('manager status'), default=False,
                                    help_text=_('Designates whether the user can manage the entire system.'))
    # Soft delete and audit fields
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', null=True, blank=True, related_name='created_users', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey('self', null=True, blank=True, related_name='updated_users', on_delete=models.SET_NULL)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
