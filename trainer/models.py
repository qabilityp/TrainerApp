from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TrainerDescription(models.Model):
    text = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

class TrainerSchedule(models.Model):
    datetime_start = models.DateTimeField(verbose_name='Datetime start', auto_now=False, null=False)
    datetime_end = models.DateTimeField(verbose_name='Datetime end', auto_now=False, null=False)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trainer.username} ({self.datetime_start} - {self.datetime_end})"

class Service(models.Model):
    LEVEL_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='Easy')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    duration = models.IntegerField()
