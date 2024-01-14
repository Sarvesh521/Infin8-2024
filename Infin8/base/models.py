from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=models.IntegerField()
    username=models.CharField(unique=True,max_length=100)
    email_token = models.CharField(max_length=255, default="")
    email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self) -> str:
        return str(self.email)
    
