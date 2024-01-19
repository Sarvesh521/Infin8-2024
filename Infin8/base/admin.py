from django.contrib import admin

# Register your models here.
from .models import User,Code,Attendance
admin.site.register(User)
admin.site.register(Code)
admin.site.register(Attendance)