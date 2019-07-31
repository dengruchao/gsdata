from django.db import models

# Create your models here.


class User(models.Model):
    key = models.CharField(max_length=200)
    times = models.IntegerField(default=0)

