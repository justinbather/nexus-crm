from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from . import models, forms


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('dashboard')

    else:
        form = forms.CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_user(request):
    user = request.user

    if request.POST:
        
        form = forms.UserForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = forms.UserForm()
        return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('../login')


def dashboard(request):
    return render(request, 'dashboard.html')