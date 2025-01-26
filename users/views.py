from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def user_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def specific_user(request, user_id):
    return HttpResponse("Hello, world. You're at the polls index.")

def login_page(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("logged_in")
        else:
            return render(request, "login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("logged_out")
    return HttpResponse('login first')

def register_page(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                        last_name=last_name)

        trainer_groups = Group.objects.get(name='Trainer')
        user.groups.add(trainer_groups)
        user.save()
        return render(request, "register.html")

