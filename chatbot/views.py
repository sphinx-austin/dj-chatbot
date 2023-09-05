from django.shortcuts import render, redirect

# third party imports
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone


# Create your views here.


def home(request):
    return render(request, 'base.html')


# AUTHENTICATION
# login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_messahe': error_message})
    else:
        return render(request, 'login.html')
