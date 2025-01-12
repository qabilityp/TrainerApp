from django.contrib import admin
from trainer.models import TrainerSchedule,TrainerDescription, Category, Service
# Register your models here.
admin.site.register(TrainerSchedule)
admin.site.register(TrainerDescription)
admin.site.register(Category)
admin.site.register(Service)