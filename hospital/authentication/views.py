# Django
from django.db.models import Sum
# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAdminUser

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
# Models
from authentication.models import (DoctorProfile,PatientProfile,Department,Appointment,Payment)
# Serializers
from authentication.serializers import (LogoutSerializer,LoginSerializer,RefreshTokenSerializer,
PaymentSerializer)
from doctor.serializers import (DoctorProfileSerializer,DepartmentSerializer)
from patient.serializers import (PatientProfileSerializer,AppointmentSerializer,UserRegSerializer)

from django.conf import settings
from .payment_utils import client

from django.http import HttpResponse

from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter

from django.views.generic import TemplateView


    
class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserRegSerializer(data=request.data)
        print("REQUEST DATA:", request.data)

        if serializer.is_valid():
            user = serializer.save()

            if user.profile.role == "doctor":
               user.is_active = False
               user.save()

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

        # BLOCK INACTIVE USERS
        if not user.is_active:
            return Response(
                {"message": "Your account is pending admin approval."},
                status=status.HTTP_403_FORBIDDEN
            )

        # BLOCK DOCTOR IF NOT APPROVED


        if hasattr(user, "doctor"):

           doctor_profile = user.doctor

           if not doctor_profile.is_approved:
              return Response(
                     {"message": "Admin approval pending. Please wait for approval."},
                     status=status.HTTP_403_FORBIDDEN
                )
    

        # DETECT ROLE SAFELY


        if user.is_staff or user.is_superuser:
           role = "admin"

        elif hasattr(user, 'doctor'):
           role = "doctor"

        elif hasattr(user, 'patient'):
            role = "patient"

        else:
            role = "user"


        # GENERATE TOKENS
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",

            "access": str(refresh.access_token),
            "refresh": str(refresh),

            "role": role,

            "user": {
                "id": user.id,
                "name": user.get_full_name(),
                "email": user.email,
                "role": role
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
        


class PatientRegisterAPIView(APIView):
    def post(self, request):
        serializer = PatientProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Patient registered successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        role = request.query_params.get("role")

        if role == "doctor":
            doctors = DoctorProfile.objects.select_related("user", "department")
            serializer = DoctorProfileSerializer(doctors, many=True)
            return Response({"doctors": serializer.data})

        elif role == "patient":
            patients = PatientProfile.objects.select_related("user")
            serializer = PatientProfileSerializer(patients, many=True)
            return Response({"patients": serializer.data})

        else:
            return Response({
                "total_doctors": DoctorProfile.objects.count(),
                "total_patients": PatientProfile.objects.count(),
                "total_departments": Department.objects.count(),
                "total_appointments": Appointment.objects.count(),
                "total_payments": Payment.objects.count()
            })



class AdminDoctorApprovalAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        try:
            doctor = DoctorProfile.objects.get(pk=pk)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

        doctor.is_approved = True
        doctor.user.is_active = True
        doctor.save()
        doctor.user.save()

        return Response({
            "message": "Doctor approved successfully"
        })          


class AdminDoctorListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        doctors = DoctorProfile.objects.select_related("user","department").all()

        serializer = DoctorProfileSerializer(doctors, many=True)

        return Response({
            "doctors": serializer.data
        })    



class AdminDoctorDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return DoctorProfile.objects.get(pk=pk)
        except DoctorProfile.DoesNotExist:
            return None

    def put(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({"error": "Not found"}, status=404)

        serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor updated successfully"})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({"error": "Not found"}, status=404)

        doctor.user.delete()  # delete user also
        return Response({"message": "Doctor deleted"}, status=204)  


    
class AdminPatientListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        patients = PatientProfile.objects.select_related("user").all()

        serializer = PatientProfileSerializer(patients, many=True)

        return Response({
            "patients": serializer.data
        })


class AdminPatientDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            patient = PatientProfile.objects.get(pk=pk)
        except PatientProfile.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        patient.user.delete()
        return Response({"message": "Patient deleted"}, status=204)    

   
    
class AdminDepartmentListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        departments = Department.objects.all()

        serializer = DepartmentSerializer(departments, many=True)

        return Response({
            "departments": serializer.data
        })        

          
class AdminDepartmentDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated"})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        department.delete()
        return Response({"message": "Deleted"}, status=204)    


    
class AdminAppointmentListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        appointments = Appointment.objects.select_related(
            "doctor","patient"
        ).order_by("-id")

        serializer = AppointmentSerializer(appointments, many=True)

        return Response({
            "appointments": serializer.data
        })    

class AdminAppointmentDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated"})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        appointment.delete()
        return Response({"message": "Deleted"}, status=204)     


            
    
class PaymentCreateAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Payment successful",
                    "data": serializer.data
                },
                status=201
            )

        return Response(serializer.errors, status=400)
    
 

class PaymentDetailAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        try:
            payment = Payment.objects.get(pk=pk)

        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)  


class CreateRazorpayOrderAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        appointment_id = request.data.get(
            "appointment_id"
        )

        try:

            appointment = Appointment.objects.get(
                id=appointment_id
            )

        except Appointment.DoesNotExist:

            return Response(
                {
                    "error":"Appointment not found"
                },
                status=404
            )

        amount = int(
            appointment.doctor.consultation_fee * 100
        )

        order = client.order.create({

            "amount": amount,

            "currency": "INR",

            "payment_capture": 1

        })

        return Response({

            "order_id": order["id"],

            "amount": amount,

            "key": settings.RAZORPAY_KEY_ID,

            "doctor":
            appointment.doctor.user.get_full_name(),

            "patient":
            appointment.patient.user.get_full_name(),

            "department":
            appointment.doctor.department.name,

            "date":
           appointment.appointment_date,

           "time":
           appointment.appointment_time

        })
    


class VerifyPaymentAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        appointment_id = request.data.get(
            "appointment_id"
        )

        try:

            appointment = Appointment.objects.get(
                id=appointment_id
            )

        except Appointment.DoesNotExist:

            return Response(
                {
                    "error":"Appointment not found"
                },
                status=404
            )

        payment = Payment.objects.create(

            appointment=appointment,

            patient=appointment.patient,

            doctor=appointment.doctor,

           amount=appointment.doctor.consultation_fee,

            payment_status="paid",

            payment_method="upi",

            transaction_id=request.data.get(
                "razorpay_payment_id"
            ),

            razorpay_order_id=request.data.get(
                "razorpay_order_id"
            ),

            razorpay_payment_id=request.data.get(
                "razorpay_payment_id"
            )

        )

        return Response({

            "message":"Payment Successful",

            "payment_id":payment.id

        })        

class PatientPaymentHistoryAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        try:

            patient = PatientProfile.objects.get(
                user=request.user
            )

        except PatientProfile.DoesNotExist:

            return Response(
                {"error": "Patient not found"},
                status=404
            )

        payments = Payment.objects.filter(
            patient=patient
        ).order_by("-created_at")

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(serializer.data)
    

    

class AdminPaymentListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        payments = Payment.objects.all()

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        total_revenue = payments.aggregate(
            total=Sum("amount")
        )["total"] or 0

        return Response({

            "payments":
            serializer.data,

            "total_revenue":
            total_revenue

        })

class DownloadInvoiceAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, payment_id):

        try:

            payment = Payment.objects.get(
                id=payment_id
            )

        except Payment.DoesNotExist:

            return Response(
                {
                    "error": "Payment not found"
                },
                status=404
            )

        response = HttpResponse(
            content_type='application/pdf'
        )

        response[
            'Content-Disposition'
        ] = f'attachment; filename="invoice_{payment.id}.pdf"'

        pdf = canvas.Canvas(
            response,
            pagesize=letter
        )

        pdf.setTitle(
            "Safe Care Invoice"
        )

        pdf.setFont(
            "Helvetica-Bold",
            20
        )

        pdf.drawString(
            200,
            760,
            "SAFE CARE HOSPITAL"
        )

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawString(
            50,
            700,
            f"Invoice ID : {payment.id}"
        )

        pdf.drawString(
            50,
            675,
            f"Patient : {payment.patient.user.get_full_name()}"
        )

        pdf.drawString(
            50,
            650,
            f"Doctor : {payment.doctor.user.get_full_name()}"
        )

        pdf.drawString(
            50,
            625,
            f"Amount : ₹{payment.amount}"
        )

        pdf.drawString(
            50,
            600,
            f"Status : {payment.payment_status}"
        )

        pdf.drawString(
            50,
            575,
            f"Payment Method : {payment.payment_method}"
        )

        pdf.drawString(
            50,
            550,
            f"Transaction ID : {payment.transaction_id}"
        )

        pdf.drawString(
            50,
            525,
            f"Date : {payment.created_at.strftime('%d-%m-%Y %H:%M')}"
        )

        pdf.line(
            50,
            500,
            550,
            500
        )

        pdf.drawString(
            50,
            470,
            "Thank you for choosing Safe Care Hospital."
        )

        pdf.save()

        return response
        

class DoctorDashboardTemplateView(TemplateView):

    template_name = "doctor-dashboard.html"    