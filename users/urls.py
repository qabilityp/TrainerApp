from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_page, name="index"),
    path("<user_id>", views.specific_user, name="specific_user"),
    path('login/', views.login_page, name='login_page'),
    path("logout/", views.logout_page, name="logout_page"),
    path("register/", views.register_page, name="register_page")
]