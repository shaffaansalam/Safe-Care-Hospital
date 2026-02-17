# from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
# from .serializers import UserRegistrationSerializer
# from .models import Patient
# from .serializers import PatientSerializer,UserProfile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import logout

from django.contrib.auth import get_user_model
User = get_user_model()



#template homepage view
def home(request):
  #rendering homepage template 
    return render(request, 'home.html')

#template aboutpage view
def about(request):
   #rendering aboutpage template 
    return render(request, 'about.html')

#template departmentspage view
def departments(request):
   #rendering departmentspage template
    return render(request, 'departments.html')

#template loginpage view
def login(request):
   #rendering loginpage template
  
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, name=name, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home.html')
        else:
            messages.error(request, "Invalid name or password.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
  

#template registerpage view
# def register(request):
   #rendering registerpage template

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
# No 'username' required anymore!
            user =  User.objects.create_user(
               
                name=form.cleaned_data['name'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )

            role = form.cleaned_data['role']

            # Create Profile
            profile = UserProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                role=role
            )

            messages.success(request, "Registration successful!")
            return redirect('home.html')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



#template contactpage view
def contact(request):
   #rendering contactpage template
    return render(request, 'contact.html')



    

