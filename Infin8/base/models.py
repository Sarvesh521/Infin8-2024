from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import pytz

TIME_ZONE = 'Asia/Kolkata'
Valid_time_limithr = 5    #in hours
Valid_time_limitmin = 2   #in minutes

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=models.CharField(max_length=10)
    username=models.CharField(unique=True,max_length=100)
    email_token = models.CharField(max_length=255, default="", blank=True)
    email_verified = models.BooleanField(default=False)
    points=models.IntegerField(default=0)
    
    worst_case_points = models.IntegerField(default=0)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']
    
    requests_left = models.IntegerField(default=15)
    def __str__(self) -> str:
        return str(self.username)
    

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


def default_valid_until():
    #return datetime.now(pytz.timezone(TIME_ZONE)) + timedelta(minutes=Valid_time_limitmin)
    return datetime.now(pytz.timezone(TIME_ZONE)) + timedelta(hours=Valid_time_limithr)

class OutgoingRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    valid_until = models.DateTimeField(default=default_valid_until)

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
    valid_until = models.DateTimeField(default=default_valid_until)
    
    game_link = models.CharField(max_length=255)
    game_status = models.CharField(max_length=255,default="pending")

    play1 = models.BooleanField(default=False)  #false if lesser than 7 else true
    play2 = models.BooleanField(default=False)
    play3 = models.BooleanField(default=False)
    points = models.IntegerField()
    
    def __str__(self) -> str:
        return str(self.game_link)
    

class Status(models.Model):
    sender_name = models.CharField(max_length=255, default="")
    receiver_name = models.CharField(max_length=255, default="")

    game_link = models.CharField(max_length=255, default="")
    game_forfeited = models.BooleanField(default=False)   #true if forfeited else false
    points = models.IntegerField(default=0)

    sender_wins = models.IntegerField(default=0)
    receiver_wins = models.IntegerField(default=0)


    def __str__(self) -> str:
        return str(self.game_link)    

