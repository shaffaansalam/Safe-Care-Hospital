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



    # ADMIN ROUTES


path('admin/dashboard/', AdminDashboardAPIView.as_view(), name='admin-dashboard'),

path('admin/doctors/approve/<int:pk>/', AdminDoctorApprovalAPIView.as_view(), name='doctor-approve'),

path('admin/doctors/', AdminDoctorListAPIView.as_view()),
path('admin/doctors/<int:pk>/', AdminDoctorDetailAPIView.as_view()),

path('admin/patients/', AdminPatientListAPIView.as_view()),
path('admin/patients/<int:pk>/', AdminPatientDetailAPIView.as_view()),

path('admin/departments/', AdminDepartmentListAPIView.as_view()),
path('admin/departments/<int:pk>/', AdminDepartmentDetailAPIView.as_view()),

path('admin/appointments/', AdminAppointmentListAPIView.as_view()),
path('admin/appointments/<int:pk>/', AdminAppointmentDetailAPIView.as_view()),

path('payments/', PaymentCreateAPIView.as_view()),

path('payments/<int:pk>/', PaymentDetailAPIView.as_view()),

path('admin/payments/', AdminPaymentReportAPIView.as_view()),


]
    
