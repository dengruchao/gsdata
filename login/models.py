from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    times = models.IntegerField(default=0)

