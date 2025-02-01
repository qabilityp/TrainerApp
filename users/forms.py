from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField

from booking.models import Booking
from trainer import models
from trainer.models import Service, TrainerSchedule, Category


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=255)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class TrainerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('category', 'level', 'duration', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select a category'

class TrainerScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainerSchedule
        fields = ['datetime_start']


