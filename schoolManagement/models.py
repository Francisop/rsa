from django.db import models
from django.conf import settings


# Create your models here.
class SchoolSession(models.Model):
    session_name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_name


class SchoolTerm(models.Model):
    term_name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class SchoolClass(models.Model):
    name = models.CharField(max_length=200)
    number_of_students = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    title = models.CharField(max_length=200)
    first_name = models.CharField(max_length=150, )
    last_name = models.CharField(max_length=150, )
    other_name = models.CharField(max_length=150, null=True, blank=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.other_name


class SchoolResult(models.Model):
    doc = models.FileField(upload_to='rsa/')
    term = models.ForeignKey(SchoolTerm, on_delete=models.CASCADE)
    term_name = models.CharField(max_length=200)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    class_name = models.CharField(max_length=200)
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matric = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
