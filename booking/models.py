from django.contrib.auth.models import User
from django.db import models

from trainer.models import Service


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer')
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trainer', 'datetime_start'], name='unique_trainer_time_slot')
        ]
