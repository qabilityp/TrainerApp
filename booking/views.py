from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def booking_page(request):
    return HttpResponse("Welcome to the booking page")

def booking_page_cancel(request, booking_id):
    return HttpResponse("Welcome to the booking page")

def booking_page_accept(request, booking_id):
    return HttpResponse("Welcome to the booking page")

def booking_page_detail(request, booking_id):
    return HttpResponse("Welcome to the booking page")

