import pytz
from django.test import TestCase
import datetime

from booking.models import Booking
from trainer.models import TrainerSchedule, TrainerDescription, Service, Category
from django.contrib.auth.models import User
from trainer import utils

class TestAvailableSlots(TestCase):
    def setUp(self):
        self.trainer = User.objects.create(username="trainer1")

    def test_empty_schedule_and_bookings(self):
        date = datetime.datetime(2022, 1, 1)
        timezone = pytz.timezone("UTC")
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        available_slots = utils.booking_time_discovery(self.trainer, date)
        start_str = start.strftime('%Y-%m-%d %H:%M')
        end_str = end.strftime('%Y-%m-%d %H:%M')
        available_slots = [slot for slot in available_slots if start_str <= slot[0] and slot[1] <= end_str]
        expected_slots = [
            ('2022-01-01 09:00', '2022-01-01 09:30'),
            ('2022-01-01 09:30', '2022-01-01 10:00'),
            ('2022-01-01 10:00', '2022-01-01 10:30'),
            ('2022-01-01 10:30', '2022-01-01 11:00'),
        ]
        self.assertEqual(available_slots, expected_slots)

    def test_schedule_with_one_event(self):
        timezone = pytz.timezone("UTC")
        date = datetime.datetime(2022, 1, 1)
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        category = Category.objects.create(name='Test Category')  # Create a test category
        service = Service.objects.create(
            category=category,  # Specify the category
            trainer=self.trainer,  # Specify the trainer
            price=12,
            duration=12
        )  # Create a test service

        user = User.objects.create_user(username='testuser', password='password123')  # Create a test user
        Booking.objects.create(
            user=user,  # Specify the user
            trainer=self.trainer,
            service=service,  # Specify the service
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 10, 30))
        )

        available_slots = utils.booking_time_discovery(self.trainer, date)
        start_str = start.strftime('%Y-%m-%d %H:%M')
        end_str = end.strftime('%Y-%m-%d %H:%M')
        available_slots = [slot for slot in available_slots if start_str <= slot[0] and slot[1] <= end_str]
        expected_slots = [
            ('2022-01-01 09:00', '2022-01-01 09:30'),
            ('2022-01-01 09:30', '2022-01-01 10:00'),
            ('2022-01-01 10:30', '2022-01-01 11:00'),
        ]
        self.assertEqual(available_slots, expected_slots)

    def test_schedule_with_two_event(self):
        timezone = pytz.timezone("UTC")
        date = datetime.datetime(2022, 1, 1)
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        category = Category.objects.create(name='Test Category')  # Create a test category
        service = Service.objects.create(
            category=category,  # Specify the category
            trainer=self.trainer,  # Specify the trainer
            price=12,
            duration=12
        )  # Create a test service

        user = User.objects.create_user(username='testuser', password='password123')  # Create a test user

        Booking.objects.create(
            user=user,  # Specify the user
            trainer=self.trainer,
            service=service,  # Specify the service
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 9, 30)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 10, 00)),
        )

        Booking.objects.create(
            user=user,  # Specify the user
            trainer=self.trainer,
            service=service,  # Specify the service
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 10, 30)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 11, 00)),
        )

        available_slots = utils.booking_time_discovery(self.trainer, date)
        start_str = start.strftime('%Y-%m-%d %H:%M')
        end_str = end.strftime('%Y-%m-%d %H:%M')
        available_slots = [slot for slot in available_slots if start_str <= slot[0] and slot[1] <= end_str]
        expected_slots = [
            ('2022-01-01 09:00', '2022-01-01 09:30'),
            ('2022-01-01 10:00', '2022-01-01 10:30'),
        ]
        self.assertEqual(available_slots, expected_slots)


    def test_schedule_with_event_at_start(self):
        timezone = pytz.timezone("UTC")
        date = datetime.datetime(2022, 1, 1)
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        category = Category.objects.create(name='Test Category')  # Create a test category
        service = Service.objects.create(
            category=category,  # Specify the category
            trainer=self.trainer,  # Specify the trainer
            price=12,
            duration=12
        )  # Create a test service

        user = User.objects.create_user(username='testuser', password='password123')  # Create a test user

        Booking.objects.create(
            user=user,  # Specify the user
            trainer=self.trainer,
            service=service,  # Specify the service
            datetime_start=start,
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
        )

        available_slots = utils.booking_time_discovery(self.trainer, date)
        start_str = start.strftime('%Y-%m-%d %H:%M')
        end_str = end.strftime('%Y-%m-%d %H:%M')
        available_slots = [slot for slot in available_slots if start_str <= slot[0] and slot[1] <= end_str]
        expected_slots = [
            ('2022-01-01 10:00', '2022-01-01 10:30'),
            ('2022-01-01 10:30', '2022-01-01 11:00'),
        ]
        self.assertEqual(available_slots, expected_slots)

    def test_schedule_with_event_at_end(self):
        timezone = pytz.timezone("UTC")
        date = datetime.datetime(2022, 1, 1)
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        category = Category.objects.create(name='Test Category')
        service = Service.objects.create(
            category=category,
            trainer=self.trainer,
            price=12,
            duration=12
        )
        user = User.objects.create_user(username='testuser', password='password123')

        Booking.objects.create(
            user=user,
            trainer=self.trainer,
            service=service,
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 11, 0)),
        )

        TrainerSchedule.objects.create(
            trainer=self.trainer,
            datetime_start=timezone.localize(datetime.datetime(2022, 1, 1, 9)),
            datetime_end=timezone.localize(datetime.datetime(2022, 1, 1, 10, 0)),
        )

        available_slots = utils.booking_time_discovery(self.trainer, date)
        start_str = start.strftime('%Y-%m-%d %H:%M')
        end_str = end.strftime('%Y-%m-%d %H:%M')
        available_slots = [slot for slot in available_slots if start_str <= slot[0] and slot[1] <= end_str]
        expected_slots = [
            ('2022-01-01 09:00', '2022-01-01 09:30'),
            ('2022-01-01 09:30', '2022-01-01 10:00'),
        ]
        self.assertEqual(available_slots, expected_slots)

    def test_schedule_with_event_spanning_entire_period(self):
        date = datetime.datetime(2022, 1, 1)

        # Create a test category
        category = Category.objects.create(name='Test Category')

        # Create a test service linked to the trainer and category
        service = Service.objects.create(
            category=category,
            trainer=self.trainer,
            price=12,
            duration=12
        )

        # Set timezone to UTC
        timezone = pytz.timezone("UTC")
        user = User.objects.create_user(username='testuser', password='password123')
        # Define the time window
        start = timezone.localize(datetime.datetime(2022, 1, 1, 9))
        end = timezone.localize(datetime.datetime(2022, 1, 1, 11))

        # Create a trainer description
        TrainerDescription.objects.create(
            trainer=self.trainer,
            text='some text',
        )

        # Create a schedule that blocks the entire period
        Booking.objects.create(
            user=user,
            trainer=self.trainer,
            service=service,
            datetime_start=start,
            datetime_end=end,
        )

        # Retrieve available booking slots
        available_slots = utils.booking_time_discovery(self.trainer, date)

        # Filter available slots within the specified time window
        start_str = start.strftime('%Y-%m-%d %H:%M')
        end_str = end.strftime('%Y-%m-%d %H:%M')
        available_slots_in_blocked_period = [
            slot for slot in available_slots if start_str <= slot[0] and slot[1] <= end_str
        ]

        # Expected result: no available slots within the fully booked period
        expected_slots = []
        self.assertEqual(available_slots_in_blocked_period, expected_slots)