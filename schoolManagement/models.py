from django.db import models


# Create your models here.
class SchoolSession(models.Model):
    session_name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.session_name


class SchoolTerm(models.Model):
    term_name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.term_name
