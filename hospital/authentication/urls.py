from django.urls import path
from .views import JWTLoginAPIView
from .views import *
from patient.views import *
from doctor.views import*
app_name='authentication'


urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    # path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/',LogoutAPIView.as_view(), name='logout'),

    path('login/', JWTLoginAPIView.as_view(), name='jwt-login'),


    path('token/refresh/', JWTRefreshAPIView.as_view(), name='jwt-refresh'),

    path('dashboard/patient/', PatientDashboardAPIView.as_view(), name='patient-dashboard'),
    path('dashboard/doctor/', DoctorDashboardAPIView.as_view(), name='doctor-dashboard'),


    # path('register/doctor/', DoctorRegisterAPIView.as_view(), name='doctor-register'),

    # path('register/patient/', PatientRegisterAPIView.as_view(), name='patient-register'),
]
    
