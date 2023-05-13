from django.contrib import admin
from .models import SchoolTerm, SchoolSession, SchoolClass, Teacher
# Register your models here.

admin.site.register(SchoolTerm)
admin.site.register(SchoolSession)
admin.site.register(SchoolClass)
admin.site.register(Teacher)

