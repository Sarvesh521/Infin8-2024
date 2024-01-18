from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=models.IntegerField()
    username=models.CharField(unique=True,max_length=100)
    email_token = models.CharField(max_length=255, default="")
    email_verified = models.BooleanField(default=False)
    points=models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self) -> str:
        return str(self.email)
    

class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_item = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.data_item    
