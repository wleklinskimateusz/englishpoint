from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(StudentGroup)
admin.site.register(StudentYear)
admin.site.register(Payment)
admin.site.register(Attendance)
admin.site.register(Year)