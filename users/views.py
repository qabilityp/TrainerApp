from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm


# Create your views here.
def user_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def specific_user(request, user_id):
    return HttpResponse("Hello, world. You're at the polls index.")

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Hello, world. You're at the polls index.")
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("Hello, world. You're at the polls index.")

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add the user to the 'Trainer' group
            trainer_group = Group.objects.get(name='Trainer')
            user.groups.add(trainer_group)
            return redirect('login_page')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

