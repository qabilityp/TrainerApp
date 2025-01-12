from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:trainer_id>/', views.trainer_page, name='trainer_page'),
    path("<int:category_id>/", views.trainer_page_category, name="trainer_page_category"),
    path("<trainer_id>/<service_id>/booking/", views.trainer_page_id_service_booking,
         name="trainer_page_service_booking")
]