
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class User(AbstractUser):
    """
    Custom user model for e-mail auth

    Do not address this model directly.
        Use RealBack.settings.AUTH_USER_MODEL on import
        and django.contrib.auth.get_user_model() on runtime
    """
    # email = models.EmailField(unique=True)
    # USERNAME_FIELD = 'email'
    pass
