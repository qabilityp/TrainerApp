from django.urls import path

from . import views

urlpatterns = [
    path("", views.trainer_page, name="index"),
    path("trainer/<category_id>", views.trainer_page_category, name="trainer_page_category"),
    path('trainer/<id>', views.trainer_page_id, name='trainer_page_id'),
    path("trainer/<id>/<service_id>", views.trainer_page_id_service, name="trainer_page_id_service"),
    path("trainer/<id>/<service_id>/booking", views.trainer_page_id_service_booking,
         name="trainer_page_id_service_booking")
]