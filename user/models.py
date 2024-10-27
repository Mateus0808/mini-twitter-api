import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('Canceled', 'Canceled'),
        ('Disabled', 'Disabled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    username = models.CharField(max_length=255, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    birth_date = models.DateField(blank=False)    
    marital_status = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'phone', 'birth_date']

    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        super().set_password(raw_password)