from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, password=None, **extra_fields):
        User.set_password(password)
        User.save(using=self._db)
        return User

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff True")
        return self.create_user(password, **extra_fields)

class User(AbstractUser):
    """ Extend the User property """
    mobile = models.CharField(max_length=15)
    verification = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'mobile']