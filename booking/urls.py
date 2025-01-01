from django.urls import path

from . import views

urlpatterns = [
    path("", views.booking_page, name="index"),
    path("/booking/<booking_id>/cancel", views.booking_page_cancel, name="booking_page_cancel"),
    path('/booking/<booking_id>/accept', views.booking_page_accept, name='booking_page_accept'),
    path("/booking/<booking_id>", views.booking_page_detail, name="booking_page_detail"),
]