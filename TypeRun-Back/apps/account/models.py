from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.create_activation_code()
        user.password = make_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, username, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **kwargs)
    
    def create_superuser(self, email, username, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create_user(email, username, password, **kwargs)

class Rank(models.TextChoices):
    f = 'F'
    d = 'D'
    c = 'C'
    b = 'B'
    a = 'A'
    s = 'S'
    ss = 'SS'
    sss = 'SSS'


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    activation_code = models.CharField(max_length=100, blank=True)
    rank = models.CharField(max_length=20, choices=Rank.choices, default=Rank.f)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects= AccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return f'{self.id}. {self.username}'
    
    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code