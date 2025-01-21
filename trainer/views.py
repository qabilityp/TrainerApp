from collections import defaultdict
from datetime import datetime, timedelta, date, time

from django.contrib import messages
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db.models import Min, Max
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.timezone import make_aware

import trainer
from booking.models import Booking
from trainer.models import TrainerDescription, Service, TrainerSchedule, Category
from trainer.utils import booking_time_discovery


# Create your views here.
def index(request):
    if request.method == 'GET':
        trainers = TrainerDescription.objects.select_related('trainer').all()
        trainers_data = []

        for trainer_description in trainers:

            my_services = Service.objects.filter(trainer=trainer_description.trainer)

            trainers_data.append({
                'trainer': trainer_description.trainer,
                'description': trainer_description.text,
                'services': my_services,
            })

        return render(request, 'trainers.html', {'trainers_data': trainers_data})

def trainer_page(request, trainer_id):
    trainer = get_object_or_404(User, id=trainer_id)

    trainer_data = get_object_or_404(TrainerDescription, trainer=trainer)

    trainer_schedule = TrainerSchedule.objects.filter(trainer=trainer).exclude(datetime_end__isnull=True)
    for schedule in trainer_schedule:
        if schedule.datetime_start is not None:
            schedule.datetime_start = make_aware(datetime.fromtimestamp(schedule.datetime_start / 1000))
        if schedule.datetime_end is not None:
            schedule.datetime_end = make_aware(datetime.fromtimestamp(schedule.datetime_end / 1000))

    trainer_services = Service.objects.filter(trainer=trainer)

    service_categories = Category.objects.all()

    return render(request, 'account.html', {
        'trainer_data': trainer_data,
        'trainer_schedule': trainer_schedule,
        'trainer_services': trainer_services,
        'service_categories': service_categories,
        'trainer': trainer,
        'user': request.user
    })

def trainer_service_page(request, trainer_id, service_id):
    current_trainer = User.objects.get(id=trainer_id)
    specific_service = Service.objects.get(id=service_id)

    if request.method == 'GET':
        available_times = {}
        days_from_now = 1
        today = make_aware(datetime.now())
        while days_from_now <= 5:
            cur_date = today + timedelta(days=days_from_now)
            available_slots = trainer.utils.booking_time_discovery(current_trainer, cur_date)
            if available_slots:
                available_times[cur_date.date()] = available_slots
            days_from_now += 1


        return render(request, "trainer_service_page.html",
                      context={'available_times': dict(available_times), 'specific_service': specific_service})

    else:
        booking_time_str = request.POST['booking-time'].strip("()").replace("'", "")
        booking_start_end = booking_time_str.split(", ")
        booking_start = datetime.strptime(booking_start_end[0],"%Y-%m-%d %H:%M")
        booking_end = datetime.strptime(booking_start_end[1],"%Y-%m-%d %H:%M")
        booking_start = make_aware(booking_start)
        booking_end = make_aware(booking_end)
        current_user = User.objects.get(id=request.user.id)
        Booking.objects.create(
            trainer=current_trainer,
            user=current_user,
            service=specific_service,
            datetime_start=booking_start,
            datetime_end=booking_end
        )
        messages.success(request, 'Your booking has been successfully created!')

        return redirect('my_bookings')

def my_bookings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    current_user = request.user
    bookings = Booking.objects.filter(user=current_user).all()
    for booking in bookings:
        booking.service_category = booking.service.category.name
    return render(request, 'success.html', context={'bookings': bookings})


def trainer_page_category(request):
    return HttpResponse("Welcome to the trainer selection page")

@login_required
def service_page(request):
    if request.method == 'GET':
        service = Service.objects.all()
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
            return redirect('/trainers/')
        else:
            return HttpResponseForbidden()

def trainer_page_id_service_booking(request):
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

