from datetime import datetime, time, timedelta

from django.utils.timezone import make_aware

from booking.models import Booking

def booking_time_discovery(trainer, date):
    start_of_day = make_aware(datetime(date.year, date.month, date.day, 8, 0, 0))
    end_of_day = make_aware(datetime(date.year, date.month, date.day, 20, 0, 0))

    available_slots = []

    current_time = start_of_day
    while current_time + timedelta(minutes=30) <= end_of_day:
        end_time = current_time + timedelta(minutes=30)

        if not Booking.objects.filter(
                trainer=trainer,
                datetime_start__lt=end_time,
                datetime_end__gt=current_time
        ).exists():
            formatted_start_time = current_time.strftime('%Y-%m-%d %H:%M')
            formatted_end_time = end_time.strftime('%Y-%m-%d %H:%M')
            available_slots.append((formatted_start_time, formatted_end_time))

        current_time = end_time

    return available_slots
