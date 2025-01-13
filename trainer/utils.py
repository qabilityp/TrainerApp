from datetime import timedelta
from re import search

import booking.models
from trainer.models import TrainerSchedule
from booking.models import Booking


def divide_time_into_15min_intervals(start, end):
    intervals = []
    current = start

    while current < end:
        next_time = current + timedelta(minutes=15)
        intervals.append({"start": current, "end": next_time, "parts": [(current, "free")]})
        current = next_time

    return intervals

def booking_time_discovery(trainer, start, end):
    schedule = TrainerSchedule.objects.filter(trainer__trainer_id=trainer, datetime_start__range=(start, end))
    bookings = Booking.objects.filter(trainer=trainer, datetime_start__range=(start, end))

    intervals = divide_time_into_15min_intervals(start, end)

    available_slots = []
    for interval in intervals:
        start_time = interval["start"]
        end_time = interval["end"]
        schedule_overlaps = schedule.filter(datetime_start__lt=end_time, datetime_end__gt=start_time)
        bookings_overlaps = bookings.filter(datetime_start__lt=end_time, datetime_end__gt=start_time)
        if not schedule_overlaps.exists() and not bookings_overlaps.exists() and end_time > start_time:
            available_slots.append((start_time, end_time))

    return available_slots

