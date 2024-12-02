from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('worker', 'Worker'),
        ('member', 'Member'),
    )
    phone = models.CharField('Phone number', max_length=15, null=True, blank=True, unique=True)
    address = models.CharField('Street address', null=True, blank=True, max_length=500)
    dob = models.DateField('Date Of Birth', null=True, blank=True)
    occupation = models.CharField(null=True, blank=True, max_length=50)
    wedding = models.DateField('Wedding date', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")

    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)