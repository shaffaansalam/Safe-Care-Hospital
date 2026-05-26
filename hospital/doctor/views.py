from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from doctor.serializers import *
from patient.serializers import *
from datetime import datetime, timedelta
from rest_framework.views import APIView
from authentication.models import DoctorProfile, Appointment,Department,Prescription,MedicalReport
from .serializers import DoctorProfileSerializer
from patient.serializers import PrescriptionSerializer,MedicalReportSerializer

from django.views.generic import TemplateView


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
            # ADD CONTEXT HERE so the serializer can build the full URL
        serializer = DoctorDashboardSerializer(doctor, context={'request': request})
        return Response(serializer.data, status=200)



class DepartmentListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Department created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class DoctorAvailableSlotsAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, doctor_id):

        try:
            doctor = DoctorProfile.objects.get(id=doctor_id, is_approved=True)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

        date_param = request.query_params.get('date')

        if not date_param:
            return Response({"error": "Date is required"}, status=400)

        date_obj = datetime.strptime(date_param, "%Y-%m-%d").date()

        start_time = doctor.available_start_time
        end_time = doctor.available_end_time

        slots = []
        current_time = datetime.combine(date_obj, start_time)

        while current_time.time() <= end_time:

            slot_time = current_time.time()

            # check if booked
            is_booked = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=date_obj,
                appointment_time=slot_time
            ).exists()

            if not is_booked:
                slots.append(slot_time.strftime("%H:%M"))

            current_time += timedelta(minutes=30)  # 30 min slot

        return Response({
            "doctor": doctor.user.get_full_name(),
            "available_slots": slots
        })    
    


class DoctorSearchAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):

        specialization = request.query_params.get('specialization')

        doctors = DoctorProfile.objects.filter(
            specialization__icontains=specialization,
            is_approved=True,
            is_available=True
        )

        serializer = DoctorProfileSerializer(doctors, many=True)

        return Response({
            "doctors": serializer.data
        })
    


class DepartmentDropdownAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):

        departments = Department.objects.all()

        data = [
            {
                "id": dept.id,
                "name": dept.name
            }
            for dept in departments
        ]

        return Response(data)    


class DepartmentDoctorsAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, department_id):

        doctors = DoctorProfile.objects.filter(
            department_id=department_id,
            is_available=True,
            is_approved=True
        )

        data = [
            {
                "id": doctor.id,
                "name": doctor.user.get_full_name(),
                "specialization": doctor.specialization,
                "fee": doctor.consultation_fee
            }
            for doctor in doctors
        ]

        return Response(data)   


# =========================================
# DOCTOR VIEW APPOINTMENTS
# =========================================

class DoctorAppointmentsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.profile.role != "doctor":

            return Response(
                {"error": "Only doctors allowed"},
                status=403
            )

        doctor = request.user.doctor

        appointments = Appointment.objects.filter(
            doctor=doctor
        ).select_related(
            'patient',
            'patient__user'
        )

        data = []

        for appointment in appointments:

            data.append({

                # IMPORTANT
                "appointment_id": appointment.id,

                # IMPORTANT
                "patient_id": appointment.patient.id,

                "patient_name":
                    appointment.patient.user.get_full_name(),

                "patient_age":
                    appointment.patient.age,

                "patient_gender":
                    appointment.patient.gender,

                "patient_blood_group":
                    appointment.patient.blood_group,

                "medical_history":
                    appointment.patient.medical_history,

                "appointment_date":
                    appointment.appointment_date,

                "appointment_time":
                    appointment.appointment_time,

                "status":
                    appointment.status,

                "reason":
                    appointment.reason
            })

        return Response(data)
    

    # =========================================
# ADD PRESCRIPTION
# =========================================

class AddPrescriptionAPIView(APIView):

    def post(self, request, appointment_id):

        try:

            appointment = Appointment.objects.get(
                id=appointment_id
            )

        except Appointment.DoesNotExist:

            return Response(
                {
                    "error": "Appointment not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        diagnosis = request.data.get("diagnosis")

        medicines = request.data.get("medicines")

        notes = request.data.get("notes")



        # CREATE / UPDATE PRESCRIPTION
        prescription, created = Prescription.objects.update_or_create(

            appointment=appointment,

            defaults={

                "diagnosis": diagnosis,

                "medicines": medicines,

                "notes": notes
            }
        )


        # =========================================
        # UPDATE APPOINTMENT STATUS
        # =========================================

        appointment.status = "completed"

        appointment.save()


        if created:

            return Response(
                {
                    "message": "Prescription Added Successfully"
                },
                status=status.HTTP_201_CREATED
            )


        return Response(
            {
                "message": "Prescription Updated Successfully"
            },
            status=status.HTTP_200_OK
        )
    

    # =========================================
# PATIENT MEDICAL HISTORY
# =========================================

class PatientMedicalHistoryAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):

        if request.user.profile.role != "doctor":

            return Response(
                {"error": "Only doctors allowed"},
                status=403
            )

        prescriptions = Prescription.objects.filter(
            appointment__patient_id=patient_id
        )

        serializer = PrescriptionSerializer(
            prescriptions,
            many=True
        )

        return Response(serializer.data)


class DoctorPatientReportsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):

        if request.user.profile.role != "doctor":

            return Response(
                {"error": "Only doctors allowed"},
                status=403
            )

        reports = MedicalReport.objects.filter(
            patient_id=patient_id
        )

        serializer = MedicalReportSerializer(
            reports,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
    

class DoctorDashboardTemplateView(TemplateView):

    template_name = "doctor-dashboard.html"    
    
