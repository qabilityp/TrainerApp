from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def trainer_page(request):
    return HttpResponse("Welcome to the trainer selection page")

def trainer_page_category(request, category_id):
    return HttpResponse("Welcome to the trainer selection page")

def trainer_page_id(request, trainer_id):
    return HttpResponse("Welcome to the trainer selection page")

def trainer_page_id_service(request, service_id):
    return HttpResponse("Welcome to the trainer selection page")

def trainer_page_id_service_booking(request, service_id):
    return HttpResponse("Welcome to the trainer selection page")