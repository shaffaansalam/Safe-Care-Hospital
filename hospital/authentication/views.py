from django.shortcuts import render
# from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.response import Response
from django.contrib.auth.models import User
from authentication.models import DoctorProfile
from authentication.serializers import LogoutSerializer,LoginSerializer
from doctor.serializers import DoctorProfileSerializer
from patient.serializers import PatientProfileSerializer
from .serializers import UserRegSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect

from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.contrib.auth import login
from django.contrib.auth import get_user_model


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RefreshTokenSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializers import UserRegSerializer
# from .serializers import DoctorProfileSerializer
from doctor.serializers import *


class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.profile.role
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class JWTLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "name": user.get_full_name(),
                "email": user.email,
                "role": user.profile.role
            }
        }, status=status.HTTP_200_OK)
    
class JWTRefreshAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh = RefreshToken(serializer.validated_data['refresh'])

            data = {
                "access": str(refresh.access_token)
            }

            # If rotation is enabled, return new refresh token
            if refresh.get('jti'):
                refresh.blacklist()
                new_refresh = RefreshToken.for_user(refresh.user)
                data["refresh"] = str(new_refresh)

            return Response(
                {
                    "message": "Token refreshed successfully",
                    **data
                },
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )    
    
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class DoctorRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                "message": "Doctor registered successfully",
                "user": serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)