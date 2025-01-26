from datetime import datetime

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from booking.models import Booking
from trainer.models import Category, Service, TrainerSchedule, TrainerDescription


# Create your tests here.
class TrainerTest(TestCase):
    def test_training(self):
        client = Client()
        response = client.get('/trainers/')
        self.assertEqual(response.status_code, 200)

    def test_booking_endpoint(self):
        # Test the booking endpoint
        trainer = User.objects.create_user(username='trainer', password='trainerpass')
        service = Service.objects.create(
            level='Medium',
            duration=60,
            price=50,
            category=Category.objects.create(name='Fitness'),
            trainer=trainer
        )

        user = User.objects.create_user(username='testuser', password='testpassword')

        client = Client()
        client.login(username='testuser', password='testpassword')

        response = client.post(f'/trainers/{trainer.id}/{service.id}/', {
            'booking-time': "(2025-01-27 10:00, 2025-01-27 11:00)"
        })

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.trainer, trainer)
        self.assertEqual(booking.user, user)
        self.assertEqual(booking.service, service)
        self.assertEqual(booking.datetime_start.replace(tzinfo=None), datetime(2025, 1, 27, 10, 0))

    def test_add_service_endpoint(self):
        # Test the endpoint for adding a service by a trainer
        group, created = Group.objects.get_or_create(name='Trainer')

        trainer = User.objects.create_user(username='trainer', password='trainerpass')
        trainer.groups.add(group)

        category = Category.objects.create(name="Test Category")

        service = Service.objects.create(
            level=1,
            duration=60,
            price=100,
            category=category,
            trainer=trainer
        )

        client = Client()
        client.login(username='trainer', password='trainerpass')

        from django.urls import reverse
        url = reverse('service_page')

        response = client.post(url, {
            'datetime_start': '2025-01-27 10:00',
            'datetime_end': '2025-01-27 11:00',
            'service': service.id,
            'add_schedule': 'true'
        })

        self.assertEqual(response.status_code, 302)

        self.assertEqual(TrainerSchedule.objects.count(), 1)
        schedule = TrainerSchedule.objects.first()
        self.assertEqual(schedule.trainer, trainer)
        self.assertEqual(schedule.datetime_start.replace(tzinfo=None), datetime(2025, 1, 27, 10, 0))
        self.assertEqual(schedule.datetime_end.replace(tzinfo=None), datetime(2025, 1, 27, 11, 0))

    def test_trainer_services_visible_only_to_trainer(self):
        group, created = Group.objects.get_or_create(name='Trainer')

        # Create users and assign the trainer group
        trainer_1 = User.objects.create_user(username='trainer1', password='trainer1pass')
        trainer_2 = User.objects.create_user(username='trainer2', password='trainer2pass')
        trainer_1.groups.add(group)
        trainer_2.groups.add(group)

        TrainerDescription.objects.create(trainer=trainer_1, text="Description for trainer_1")
        TrainerDescription.objects.create(trainer=trainer_2, text="Description for trainer_2")

        # Create categories and services
        category = Category.objects.create(name="Fitness")
        Service.objects.create(level='Medium', duration=60, price=100, category=category, trainer=trainer_1)
        Service.objects.create(level='Easy', duration=30, price=50, category=category, trainer=trainer_2)

        client = Client()
        client.login(username='trainer1', password='trainer1pass')

        response = client.get('/service/')

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Fitness')





