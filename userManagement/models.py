from contextlib import nullcontext

from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# import rest_framework.authtoken.models
# import rest_framework.authentication
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from cloudinary.models import CloudinaryField

from schoolManagement.models import SchoolClass, SchoolSession


# User = get_user_model()


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, first_name,last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, first_name,last_name, password, **other_fields)

    def create_user(self, username, first_name,last_name, password, **other_fields):

        other_fields.setdefault('is_active', True)

        if not username:
            raise ValueError(_('You must provide a username'))

        username = username
        user = self.model(username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'admin'),
        ('student', 'student'),
    )

    GENDER = (
        ('male', 'm'),
        ('female', 'f'),
    )

    username = models.CharField(_('username'), max_length=20, unique=True, null=True,blank=True)
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    other_name = models.CharField(max_length=150, null=True, blank=True)
    role = models.CharField(max_length=150, choices=ROLES, default="admin")
    gender = models.CharField(max_length=150, choices=GENDER)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE, null=True, blank=True)
    matric = models.CharField(max_length=150, null=True, blank=True, unique=True)
    dp = models.ImageField(upload_to='images')
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

