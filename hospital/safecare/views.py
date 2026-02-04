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


#API


# class UserRegistrationAPI(ModelViewSet):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "User registered successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PatientViewSet(APIView):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
# # #     permission_classes = [IsPatient]

# class UserRegistrationAPI(APIView):
#     permission_classes=[AllowAny]
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "message": "Patient registered successfully",
#                     "data": serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserRegistrationAPI(APIView):
#     # 'name' is what they type in the 'Name' box
#     name = serializers.CharField(max_length=150, write_only=True)

#     role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='patient')
#     email = serializers.EmailField(
#         max_length=100,
#         validators=[UniqueValidator(queryset=User.objects.all(), message="A user with this email already exists.")]
#     )
#     password = serializers.CharField(write_only=True, min_length=8)

#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password', 'role']

#     def create(self, validated_data):
#         name = validated_data.pop('name')
#         role = validated_data.pop('role')
#         email = validated_data.get('email')
        
#         # FIX: Since Django REQUIRES a unique username, we use the Email as the username.
#         # This allows multiple people to have the same 'First Name' or 'Display Name'.
#         user = User.objects.create_user(
#             first_name=name, # Storing their preferred name here
#             **validated_data
#         )

#         UserProfile.objects.create(user=user, role=role.lower())
#         return user
    

# class LoginAPI(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         name = request.data.get('name')
#         password = request.data.get('password')

    
#         user = authenticate(name=name, password=password)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'Login successful',
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'user': {
#                     'name': user.first_name,
#                     'email': user.email,
#                     'role': user.userprofile.role # Assuming your profile has this related name
#                 }
#             }, status=status.HTTP_200_OK)
        
#         return Response({'error': 'Invalid Name or Password'}, status=status.HTTP_401_UNAUTHORIZED)
    

