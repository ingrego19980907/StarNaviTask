import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


class CustomUserManager(UserManager):

    def get_email(self):
        """Return the username for this User."""
        return getattr(self, self.EMAIL_FIELD)

    def create_user(self, email, username=None, password=None, **extra_fields):
        username_or_email = username or email
        return super().create_user(email=email, username=username_or_email,
                                   password=password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        username_or_email = username or email
        return super().create_superuser(email=email, username=username_or_email,
                                        password=password, **extra_fields)


class EmailRequiredUser(AbstractUser):
    """
    Username, Email and password are required. Other fields are optional.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True,
                              blank=False, null=False)
    full_name = models.TextField(_("full name"), blank=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        blank=True,
        null=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[AbstractUser.username_validator],
    )
    last_password_changed = models.DateTimeField(default=timezone.now)
    last_request = models.DateTimeField(verbose_name='last request', blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
