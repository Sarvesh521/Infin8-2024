from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=models.IntegerField()
    username=models.CharField(unique=True,max_length=100)
    email_token = models.CharField(max_length=255, default="", blank=True)
    email_verified = models.BooleanField(default=False)
    points=models.IntegerField(default=0)
    
    worst_case_points = models.IntegerField(default=0)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']
    
    requests_left = models.IntegerField(default=5)
    def __str__(self) -> str:
        return str(self.email)
    

class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_item = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.data_item    

class Attendance(models.Model):
    code=models.CharField(max_length=255)
    value=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.code
    

class OutgoingRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)

    game_link = models.CharField(max_length=255)
    game_status = models.CharField(max_length=255,default="pending")

    num1 = models.IntegerField()
    num2 = models.IntegerField()
    num3 = models.IntegerField()
    points = models.IntegerField()

    turn = models.IntegerField(default=1)
    wins = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.game_link)
    

class IncomingRequest(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)

    request_time = models.DateTimeField(auto_now_add=True)
    game_link = models.CharField(max_length=255)
    game_status = models.CharField(max_length=255,default="pending")

    num1 = models.IntegerField()
    num2 = models.IntegerField()
    num3 = models.IntegerField()
    points = models.IntegerField()
    
    def __str__(self) -> str:
        return str(self.game_link)