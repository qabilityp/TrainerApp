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

from booking.models import Booking
from trainer.forms import TrainerScheduleForm
from trainer.models import TrainerDescription, Service, TrainerSchedule, Category
from trainer.utils import booking_time_discovery
from users.forms import TrainerRegisterForm, ServiceForm


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

    trainer_schedule = TrainerSchedule.objects.filter(trainer=trainer)

    schedules = TrainerSchedule.objects.filter(datetime_end__isnull=True)

    # Update them with a calculated datetime_end (1 hour after datetime_start)
    for schedule in schedules:
        if schedule.datetime_start:
            schedule.datetime_end = schedule.datetime_start + timedelta(hours=1)
            schedule.save()

    # Verify the updates
    for schedule in schedules:
        print(f"Schedule ID: {schedule.id}, Start: {schedule.datetime_start}, End: {schedule.datetime_end}")

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
            available_slots = booking_time_discovery(current_trainer, cur_date)
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
    if not request.user.groups.filter(name='Trainer').exists():
        return HttpResponseForbidden("You are not a trainer")

    trainer_current = request.user

    if request.method == 'POST':
        if 'add_service' in request.POST:  # Добавление услуги
            service_form = ServiceForm(request.POST)
            if service_form.is_valid():
                service = service_form.save(commit=False)
                service.trainer = trainer_current
                service.save()
            else:
                return render(request, 'trainer.html', {
                    'trainer': trainer_current,
                    'service_form': service_form,
                })
        elif 'add_schedule' in request.POST:  # Добавление расписания
            schedule_form = TrainerScheduleForm(request.POST)
            if schedule_form.is_valid():
                schedule = schedule_form.save(commit=False)
                schedule.trainer = trainer_current
                schedule.save()
            else:
                return render(request, 'trainer.html', {
                    'trainer': trainer_current,
                    'schedule_form': schedule_form,
                })
        return redirect('service_page')
    else:
        trainer_description = TrainerDescription.objects.get(trainer=trainer_current)
        trainer_schedule = TrainerSchedule.objects.filter(trainer=trainer_current)
        my_services = Service.objects.filter(trainer=trainer_current)
        service_categories = Category.objects.all()

        service_form = ServiceForm()
        schedule_form = TrainerScheduleForm()

        return render(request, 'trainer.html', {
            'trainer': trainer_current,
            'trainer_description': trainer_description,
            'trainer_schedule': trainer_schedule,
            'my_services': my_services,
            'service_categories': service_categories,
            'service_form': service_form,
            'schedule_form': schedule_form,
        })


def trainer_page_id_service_booking(request):
    return HttpResponse("Welcome to the trainer selection page")

def trainer_register(request):
    if request.method == 'POST':
        form = TrainerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not request.user.groups.filter(name='Trainer').exists():
                trainer_group = Group.objects.get(name='Trainer')
                user.groups.add(trainer_group)
                user.save()
            messages.success(request, 'Trainer registration successful!')
            return HttpResponse("Trainer registration successful")
    else:
        form = TrainerRegisterForm()
    return render(request, 'trainer_signup.html', {'form': form})

