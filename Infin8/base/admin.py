from django.contrib import admin

# Register your models here.
from .models import User,Code,Attendance, IncomingRequest, OutgoingRequest
admin.site.register(User)
admin.site.register(Code)
admin.site.register(Attendance)
admin.site.register(OutgoingRequest)
admin.site.register(IncomingRequest)
