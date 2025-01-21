import pytz
from django.test import TestCase
import datetime

from trainer.models import TrainerSchedule, TrainerDescription
from django.contrib.auth.models import User
from trainer import utils

class TestAvailableSlots(TestCase):
    def setUp(self):
        self.trainer = User.objects.create(username="trainer1")

    def test_empty_schedule_and_bookings(self):
        timezone = pytz.timezone("UTC")
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        available_slots = utils.booking_time_discovery(self.trainer.id, start, end)
        expected_slots = [
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 0)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 15))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 15)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 30))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 45))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 45)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 0))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 15))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 15)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 30))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 45))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 45)),
             timezone.localize(datetime.datetime(2022, 1, 1, 11, 0))),
        ]
        result = utils.booking_time_discovery(self.trainer.id, start, end)
        self.assertEqual(available_slots, expected_slots, result)

    def test_schedule_with_one_event(self):
        timezone = pytz.timezone("UTC")
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        trainer_description = TrainerSchedule.objects.create(
            trainer=User.objects.get(id=1),
            datetime_start=datetime.datetime(2022, 1, 1, 10, 0, 0),
            datetime_end=datetime.datetime(2022, 1, 1, 11, 0, 0),
        )

        TrainerSchedule.objects.create(
            trainer_id=trainer_description.id,
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 10, 30)),
        )

        available_slots = utils.booking_time_discovery(self.trainer.id, start, end)
        expected_slots = [
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 0)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 15))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 15)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 30))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 45))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 45)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 0))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 45))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 45)),
             timezone.localize(datetime.datetime(2022, 1, 1, 11, 0))),
        ]
        result = utils.booking_time_discovery(self.trainer.id, start, end)
        self.assertEqual(available_slots, expected_slots, result)

    def test_schedule_with_two_event(self):
        timezone = pytz.timezone("UTC")
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        trainer_description = TrainerDescription.objects.create(
            trainer=self.trainer,
        )

        TrainerSchedule.objects.create(
            trainer_id=trainer_description.id,
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 10, 30)),
        )

        TrainerSchedule.objects.create(
            trainer_id=trainer_description.id,
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 10, 45)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 11, 0)),
        )

        available_slots = utils.booking_time_discovery(self.trainer.id, start, end)
        expected_slots = [
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 0)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 15))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 15)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 30))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 45))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 45)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 0))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 45))),
        ]
        result = utils.booking_time_discovery(self.trainer.id, start, end)
        self.assertEqual(available_slots, expected_slots, result)

    def test_schedule_with_event_at_start(self):
        timezone = pytz.timezone("UTC")
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        trainer_description = TrainerDescription.objects.create(
            trainer=self.trainer,
            text='some text',
        )
        TrainerSchedule.objects.create(
            trainer=trainer_description,
            datetime_start=start,
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
        )

        available_slots = utils.booking_time_discovery(self.trainer.id, start, end)
        expected_slots = [
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 15))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 15)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 30))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 45))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 10, 45)),
             timezone.localize(datetime.datetime(2022, 1, 1, 11, 0))),
        ]
        self.assertEqual(available_slots, expected_slots)

    def test_schedule_with_event_at_end(self):
        timezone = pytz.timezone("UTC")
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        trainer_description = TrainerDescription.objects.create(
            trainer=self.trainer,
            text='some text',
        )
        TrainerSchedule.objects.create(
            trainer=trainer_description,
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
            datetime_end=end,
        )

        available_slots = utils.booking_time_discovery(self.trainer.id, start, end)
        expected_slots = [
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 0)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 15))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 15)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 30))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 30)),
             timezone.localize(datetime.datetime(2022, 1, 1, 9, 45))),
            (timezone.localize(datetime.datetime(2022, 1, 1, 9, 45)),
             timezone.localize(datetime.datetime(2022, 1, 1, 10, 0))),
        ]
        self.assertEqual(available_slots, expected_slots)

    def test_schedule_with_event_spanning_entire_period(self):
        timezone = pytz.timezone("UTC")
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        trainer_description = TrainerDescription.objects.create(
            trainer=self.trainer,
            text='some text',
        )
        TrainerSchedule.objects.create(
            trainer=trainer_description,
            datetime_start=start,
            datetime_end=end,
        )

        available_slots = utils.booking_time_discovery(self.trainer.id, start, end)
        expected_slots = []
        self.assertEqual(available_slots, expected_slots)