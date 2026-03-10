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
from doctor.serializers import (DoctorProfileSerializer,DepartmentSerializer,DoctorRegistrationSerializer)
from patient.serializers import (PatientProfileSerializer,AppointmentSerializer,UserRegSerializer)


    
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

# class RegisterApi(APIView):

#     permission_classes = [AllowAny]

#     def post(self, request):

#         role = request.data.get("role")

#         if role == "doctor":
#             serializer = DoctorRegistrationSerializer(data=request.data)

#         elif role == "patient":
#             serializer = UserRegSerializer(data=request.data)

#         else:
#             return Response(
#                 {"error": "Invalid role"},
#                 status=400
#             )

#         if serializer.is_valid():
#             user = serializer.save()

#             return Response(
#                 {
#                     "message": f"{role.capitalize()} registered successfully",
#                     "user": {
#                         "id": user.id,
#                         "email": user.email,
#                         "role": role
#                     }
#                 },
#                 status=201
#             )

#         return Response(serializer.errors, status=400)        
   

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
        if user.profile.role == "doctor":

            doctor_profile = getattr(user, "doctor", None)

            if doctor_profile and not doctor_profile.is_approved:
                return Response(
                    {"message": "Admin approval pending. Please wait for approval."},
                    status=status.HTTP_403_FORBIDDEN
                )

        # DETECT ROLE SAFELY
        if hasattr(user, 'doctor'):
            role = "doctor"
        elif hasattr(user, 'patient'):
            role = "patient"
        elif user.is_staff:
            role = "admin"
        else:
            role = user.profile.role

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



# class JWTLoginAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']

#         #  BLOCK DOCTOR IF NOT APPROVED
#          #  BLOCK INACTIVE USERS (Doctor not approved)
#         if not user.is_active:
#             return Response(
#                 {
#                     "message": "Your account is pending admin approval."
#                 },
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         if user.profile.role == "doctor":
#             # doctor_profile = getattr(user, "doctorprofile", None)
#             doctor_profile = getattr(user, "doctor", None)

#             if doctor_profile and not doctor_profile.is_approved:
#                 return Response(
#                     {
#                         "message": "Admin approval pending. Please wait for approval."
#                     },
#                     status=status.HTTP_403_FORBIDDEN
#                 )

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "message": "Login successful",
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": {
#                 "id": user.id,
#                 "name": user.get_full_name(),
#                 "email": user.email,
#                 "role": user.profile.role
#             }
#         }, status=status.HTTP_200_OK)
    
    

    
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
            serializer.save()  # doctor created, is_approved=False

            return Response(
                {
                    "message": "Doctor registered successfully. Await admin approval."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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

        doctors = DoctorProfile.objects.all()
        patients = PatientProfile.objects.all()
        departments = Department.objects.all()
        appointments = Appointment.objects.all().order_by('-id')[:5]
        payments = Payment.objects.all()

        doctor_serializer = DoctorProfileSerializer(doctors, many=True)
        patient_serializer = PatientProfileSerializer(patients, many=True)
        appointment_serializer = AppointmentSerializer(appointments, many=True)

        total_revenue = payments.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "doctors": doctor_serializer.data,
            "patients": patient_serializer.data,
            "departments": departments.count(),
            "appointments": appointment_serializer.data,
            "payments": total_revenue
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
        doctors = DoctorProfile.objects.all()
        serializer = DoctorProfileSerializer(doctors, many=True)
        return Response(serializer.data)



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
        patients = PatientProfile.objects.all()
        serializer = PatientProfileSerializer(patients, many=True)
        return Response(serializer.data)

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
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        

          
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
        appointments = Appointment.objects.all().order_by('-created_at')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

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
    
class AdminPaymentReportAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        payments = Payment.objects.all().order_by('-created_at')

        serializer = PaymentSerializer(payments, many=True)

        return Response(serializer.data)    

class PaymentDetailAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        try:
            payment = Payment.objects.get(pk=pk)

        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)    