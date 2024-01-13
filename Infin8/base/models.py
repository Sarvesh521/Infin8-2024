from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    phone_number=models.IntegerField(null=True)
    username=models.CharField(unique=True,max_length=100,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self) -> str:
        return str(self.email)

