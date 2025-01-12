from datetime import timedelta
from re import search

import booking


def divide_time_into_15min_intervals(trainer, start_time, end_time):
    trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer, datetime_start__date=start_time,
                                                                     datetime_end__date=end_time)
    thirty_mins = timedelta(minutes=15)
    divided_schedule = []

    for entry in trainer_schedule:
        start = entry.datetime_start
        end = entry.datetime_end
        parts = divide_time_into_15min_intervals(start, end)
        divided_schedule.extend(parts)

    return divided_schedule

def booking_time_discovery(trainer, service_id, date):
    trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer, datetime_start__date=date)
    trainer_bookings = booking.models.Booking.objects.filter(trainer=trainer, datetime_start__date=date)
    desired_service = trainer.models.Service.objects.get(pk=service_id)
    search_window = desired_service.duration

    divided_schedule = divide_time_into_15min_intervals(trainer, date, date + timedelta(days=1))

    available_slots = []
    for entry in divided_schedule:
        start = entry["start"]
        end = entry["end"]
        duration = end - start

        if search_window <= duration:
            parts = entry["parts"]
            for part, status in parts:
                if status == "Свободно":
                    available_slots.append(part, duration)
                    break

    return available_slots


