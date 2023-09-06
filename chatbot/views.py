from django.shortcuts import render, redirect

# third party imports
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Chat
import openai
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Create your views here.

openai_api_key = os.getenv('OPENAI_API_KEY')

# openai API


def ask_openai(message):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=[
            {'role': 'system', 'content': 'You are an helpful assistant'},
            {'role': 'user', 'content': message}
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer


# chatbot view
@login_required(login_url='login')
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message,
                    response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})


# AUTHENTICATION

# login


def login(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(
                request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('chatbot')
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_messahe': error_message})
        else:
            return render(request, 'login.html')

# regitration


def register(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 == password2:
                try:
                    user = User.objects.create_user(username, email, password1)
                    user.save()
                    auth.login(request, user)
                    return redirect('chatbot')
                except:
                    error_message = 'Error creating account'
                    return render(request, 'register.html', {'error_message': error_message})
        return render(request, 'register.html')


# logout

def logout(request):
    auth.logout(request)
    return redirect('login')
