from django.contrib import admin

# Register your models here.
from .models import User,Code
admin.site.register(User)
admin.site.register(Code)