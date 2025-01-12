from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class TrainerDescription(models.Model):
    text = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

class TrainerSchedule(models.Model):
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    trainer = models.ForeignKey(TrainerDescription, on_delete=models.CASCADE)

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