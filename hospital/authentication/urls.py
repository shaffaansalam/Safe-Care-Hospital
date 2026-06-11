from django.urls import path
from .views import JWTLoginAPIView
from .views import *
from patient.views import *
from doctor.views import*

app_name='authentication'


urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),

    
    path('logout/',LogoutAPIView.as_view(), name='logout'),

    path('login/', JWTLoginAPIView.as_view(), name='jwt-login'),


    path('token/refresh/', JWTRefreshAPIView.as_view(), name='jwt-refresh'),

    path('dashboard/patient/', PatientDashboardAPIView.as_view(), name='patient-dashboard'),
    path('dashboard/doctor/', DoctorDashboardAPIView.as_view(), name='doctor-dashboard'),



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

path('admin/payments/',AdminPaymentListAPIView.as_view()),

path('doctor/<int:doctor_id>/slots/', DoctorAvailableSlotsAPIView.as_view()),

path('appointments/book/', BookAppointmentAPIView.as_view()),

path('appointments/my/', PatientAppointmentsAPIView.as_view()),
path('appointments/cancel/<int:appointment_id>/',CancelAppointmentAPIView.as_view()),
path('appointments/reschedule/<int:appointment_id>/',RequestRescheduleAPIView.as_view()),

path('departments/dropdown/',DepartmentDropdownAPIView.as_view(),),

path('departments/<int:department_id>/doctors/',DepartmentDoctorsAPIView.as_view(),),

path('doctors/search/',DoctorSearchAPIView.as_view(),name='doctor-search'),

path('doctor/appointments/',DoctorAppointmentsAPIView.as_view()),
path('doctor/appointment-status/<int:appointment_id>/',UpdateAppointmentStatusAPIView.as_view()),
path('doctor/reschedule-appointment/<int:appointment_id>/',RescheduleAppointmentAPIView.as_view()),

path('doctor/prescription/<int:appointment_id>/',AddPrescriptionAPIView.as_view()),

path('doctor/patient-history/<int:patient_id>/',PatientMedicalHistoryAPIView.as_view()),

path('patient/prescriptions/',PatientPrescriptionsAPIView.as_view()),

path('prescription/pdf/<int:pk>/',PrescriptionPDFAPIView.as_view()),

path('patient/reports/',PatientReportsAPIView.as_view()),

path('doctor/request-test/<int:appointment_id>/',RequestMedicalTestAPIView.as_view()),

path('patient/test-requests/',PatientTestRequestsAPIView.as_view()),

path('patient/upload-report/<int:test_request_id>/',PatientUploadReportAPIView.as_view()),

path('doctor/patient-reports/<int:patient_id>/',DoctorPatientReportsAPIView.as_view()),

path('patient/profile/update/',PatientProfileUpdateAPIView.as_view(),name='patient-profile-update'),

path('doctor/profile/update/',DoctorProfileUpdateAPIView.as_view(),name='doctor-profile-update'),

path('patient/profile/',PatientProfileAPIView.as_view(),name='patient-profile'),

path('doctor/profile/',DoctorProfileAPIView.as_view(),name='doctor-profile'),

path("payments/create-order/",CreateRazorpayOrderAPIView.as_view()),

path("payments/verify/",VerifyPaymentAPIView.as_view()),

path("payments/history/",PatientPaymentHistoryAPIView.as_view()),

path("payments/invoice/<int:payment_id>/",DownloadInvoiceAPIView.as_view()),



]
    
