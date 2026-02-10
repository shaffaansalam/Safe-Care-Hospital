from django.urls import path
from .views import JWTLoginAPIView
from .views import *
app_name='authentication'

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    # path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/',LogoutAPIView.as_view(), name='logout'),

    path('login/', JWTLoginAPIView.as_view(), name='jwt-login'),
    path('token/refresh/', JWTRefreshAPIView.as_view(), name='jwt-refresh'),

    # path('register/doctor/', DoctorRegisterAPIView.as_view(), name='doctor-register'),

    # path('register/patient/', PatientRegisterAPIView.as_view(), name='patient-register'),
]
    
