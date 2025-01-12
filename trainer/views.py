from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404

import booking
import trainer
from trainer.models import TrainerDescription, Service
from trainer.utils import booking_time_discovery


# Create your views here.
def index(request):
    service_categories = trainer.models.Category.objects.all()
    my_services = trainer.models.Service.objects.filter(trainer=request.user).all()
    return render(request, 'trainer.html', {'service_categories': service_categories,
                                                'my_services': my_services})

def trainer_page(request, trainer_id=None, service_id=None):
    if request.user.groups.filter(name='Trainer').exists():
        if request.method == 'GET':
            service_categories = trainer.models.Category.objects.all()
            my_services = trainer.models.Service.objects.filter(trainer=request.user).all()
            return render(request, 'trainer.html', {'service_categories': service_categories,
                                                    'my_services': my_services})
        return HttpResponse('Hello , trainer page')
    else:
        trainer_data = get_object_or_404(TrainerDescription, pk=trainer_id)
        trainer_user = trainer_data.trainer

        trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer_data)

        trainer_services = trainer.models.Service.objects.filter(trainer=trainer_user)

        available_slots = []
        if service_id:
            desired_service = get_object_or_404(Service, pk=service_id)
            available_slots = booking_time_discovery(trainer_user, service_id)
        context = {
            'user': request.user,
            'trainer_data': trainer_data,
            'trainer_schedule': trainer_schedule,
            'available_slots': available_slots,
            'trainer_services': trainer_services,
        }
    print(f"Trainer Data: {trainer_data}")
    print(f"Trainer Schedule: {trainer_schedule}")
    print(f"Available Slots: {available_slots}")
    print(f"Trainer Services: {trainer_services}")

    return render(request, 'account.html', {'context': context})


def trainer_page_category(request, category_id):
    return HttpResponse("Welcome to the trainer selection page")

@login_required
def service_page(request):
    if request.method == 'GET':
        service = trainer.Service.objects.all()
        service_categories = trainer.models.Category.objects.all()
        return render(request, 'services.html', {'service': service,
                                                 'service_categories': service_categories})
    if request.method == "POST":
        if request.user.groups.filter(name='Trainer').exists():
            form_data = request.POST
            service_categories = trainer.models.Category.objects.get(pk=form_data['category'])
            service = trainer.models.Service(
                level=form_data['level'],
                duration=form_data['duration'],
                price=form_data['price'],
                category=service_categories,
                trainer=request.user,
            )
            service.save()
            return redirect('/trainer/')
        else:
            return HttpResponseForbidden()

def trainer_page_id_service_booking(request, service_id):
    return HttpResponse("Welcome to the trainer selection page")

def trainer_register(request):
    if request.user.groups.filter(name='Trainer').exists():
        if request.method == 'GET':
            return render(request, 'trainer_signup.html')
        else:
            if request.user.groups.filter(name='Trainer').exists():
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']

                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                                last_name=last_name)

                trainer_group = Group.objects.get(name='Trainer')
                user.groups.add(trainer_group)
                user.save()
                return HttpResponse("Trainer registration successful")

