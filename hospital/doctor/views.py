from django.shortcuts import render

# from .forms import RegisterForm

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework.response import Response

# from .serializers import DoctorProfileSerializer
from doctor.serializers import *
from patient.serializers import *

# Create your views here.



class DoctorDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.profile.role != "doctor":
            return Response({"error": "Unauthorized"}, status=403)

        doctor = request.user.doctor

        if not doctor.is_approved:
            return Response(
                {"message": "Admin approval pending"},
                status=403
            )

        serializer = DoctorDashboardSerializer(doctor)
        return Response(serializer.data, status=200)
