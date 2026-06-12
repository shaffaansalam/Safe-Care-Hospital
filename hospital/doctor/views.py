from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from doctor.serializers import *
from patient.serializers import *
from datetime import datetime, timedelta
from rest_framework.views import APIView
from authentication.models import DoctorProfile, Appointment,Department,Prescription,MedicalReport,Notification
from .serializers import DoctorProfileSerializer,DoctorProfileUpdateSerializer
from patient.serializers import PrescriptionSerializer,MedicalReportSerializer
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from reportlab.pdfgen import canvas


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


class DoctorProfileUpdateAPIView(
    generics.UpdateAPIView
):

    serializer_class = (
        DoctorProfileUpdateSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def get_object(self):

        return self.request.user.doctor
    

class DoctorProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        doctor = request.user.doctor

        serializer = DoctorProfileSerializer(doctor)

        return Response(serializer.data)
    

class DoctorAvailabilityToggleAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):

        if request.user.profile.role != "doctor":

            return Response(
                {"error": "Only doctors allowed"},
                status=403
            )

        doctor = request.user.doctor

        doctor.is_available = not doctor.is_available

        doctor.save()

        return Response({

            "message": "Availability updated",

            "is_available": doctor.is_available

        })
    

    

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
    

class UpdateAppointmentStatusAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, appointment_id):

        if request.user.profile.role != "doctor":

            return Response(
                {"error": "Only doctors allowed"},
                status=403
            )

        try:

            appointment = Appointment.objects.get(
                id=appointment_id,
                doctor=request.user.doctor
            )

        except Appointment.DoesNotExist:

            return Response(
                {"error": "Appointment not found"},
                status=404
            )

        status_value = request.data.get("status")

        if status_value not in ["accepted", "rejected","completed"]:

            return Response(
                {"error": "Invalid status"},
                status=400
            )

        appointment.status = status_value

        appointment.save()

        if status_value == "accepted":
             
             print(
                  "PATIENT USER:",
                  appointment.patient.user.id
                   )

             Notification.objects.create(

             user=appointment.patient.user,

             title="Appointment Accepted",

             message=f"Dr. {appointment.doctor.user.get_full_name()} accepted your appointment."

             )

        elif status_value == "rejected":

          Notification.objects.create(

          user=appointment.patient.user,

          title="Appointment Rejected",

           message=f"Dr. {appointment.doctor.user.get_full_name()} rejected your appointment."

          )

        return Response({

            "message":
            f"Appointment {status_value} successfully"

        })
    
class RescheduleAppointmentAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, appointment_id):

        if request.user.profile.role != "doctor":

            return Response(
                {"error": "Only doctors allowed"},
                status=403
            )

        try:

            appointment = Appointment.objects.get(
                id=appointment_id,
                doctor=request.user.doctor
            )

        except Appointment.DoesNotExist:

            return Response(
                {"error": "Appointment not found"},
                status=404
            )

        if appointment.status != "accepted":

            Notification.objects.create(

            user=appointment.patient.user,

           title="Appointment Accepted",

           message=f"Dr. {appointment.doctor.user.get_full_name()} accepted your appointment."

        )

            return Response(
                {
                    "error":
                    "Only accepted appointments can be rescheduled"
                },
                status=400
            )

        new_date = request.data.get("appointment_date")

        new_time = request.data.get("appointment_time")

        if not new_date or not new_time:

            return Response(
                {
                    "error":
                    "Date and time required"
                },
                status=400
            )

        # Check slot availability

        existing = Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=new_date,
            appointment_time=new_time
        ).exclude(id=appointment.id)

        if existing.exists():

            return Response(
                {
                    "error":
                    "Selected slot already booked"
                },
                status=400
            )



        appointment.old_appointment_date = appointment.appointment_date

        appointment.old_appointment_time = appointment.appointment_time

        appointment.appointment_date = new_date

        appointment.appointment_time = new_time

        appointment.rescheduled = True

        appointment.save()

        return Response({

            "message":
            "Appointment rescheduled successfully",

            "appointment_date":
            appointment.appointment_date,

            "appointment_time":
            appointment.appointment_time

        })
    

    # =========================================
# ADD PRESCRIPTION
# =========================================

class AddPrescriptionAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

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

        # CREATE OR UPDATE PRESCRIPTION

        prescription, created = Prescription.objects.update_or_create(

            appointment=appointment,

            defaults={
                "diagnosis": diagnosis,
                "medicines": medicines,
                "notes": notes
            }
        )

        Notification.objects.create(

        user=appointment.patient.user,

        title="Prescription Uploaded",

        message=f"Dr. {appointment.doctor.user.get_full_name()} uploaded your prescription."

        )


        # =========================================
        # SEND PROFESSIONAL HTML EMAIL
        # =========================================

        try:

            patient_email = appointment.patient.user.email

            patient_name = appointment.patient.user.get_full_name()

            doctor_name = appointment.doctor.user.get_full_name()

            subject = "Safe Care Hospital - Prescription Details"

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;">

                <div style="max-width:800px;margin:30px auto;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 0 15px rgba(0,0,0,0.1);">

                    <!-- HEADER -->

                    <div style="background:#0d6efd;padding:25px;text-align:center;color:white;">

                        <h1 style="margin:0;">
                            Safe Care Hospital
                        </h1>

                        <p style="margin-top:10px;">
                            Digital Healthcare Management System
                        </p>

                    </div>

                    <!-- BODY -->

                    <div style="padding:30px;">

                        <h2>
                            Hello {patient_name},
                        </h2>

                        <p>
                            Your consultation has been completed successfully.
                            Please find your prescription details below.
                        </p>

                        <!-- DOCTOR CARD -->

                        <div style="
                            background:#e8f1ff;
                            border-left:5px solid #0d6efd;
                            padding:15px;
                            margin-top:20px;
                            border-radius:8px;
                        ">

                            <h3 style="margin-top:0;">
                                Doctor Information
                            </h3>

                            <p>
                                <strong>Doctor:</strong>
                                {doctor_name}
                            </p>

                        </div>

                        <!-- DIAGNOSIS CARD -->

                        <div style="
                            background:#e8f5e9;
                            border-left:5px solid #28a745;
                            padding:15px;
                            margin-top:20px;
                            border-radius:8px;
                        ">

                            <h3 style="margin-top:0;">
                                Diagnosis
                            </h3>

                            <p>
                                {diagnosis}
                            </p>

                        </div>

                        <!-- MEDICINES TABLE -->

                        <div style="margin-top:20px;">

                            <h3>
                                Prescribed Medicines
                            </h3>

                            <table style="
                                width:100%;
                                border-collapse:collapse;
                            ">

                                <tr style="background:#0d6efd;color:white;">

                                    <th style="padding:12px;border:1px solid #ddd;">
                                        Medicines
                                    </th>

                                </tr>

                                <tr>

                                    <td style="padding:12px;border:1px solid #ddd;">
                                        {medicines}
                                    </td>

                                </tr>

                            </table>

                        </div>

                        <!-- NOTES -->

                        <div style="
                            background:#fff3cd;
                            border-left:5px solid #ffc107;
                            padding:15px;
                            margin-top:20px;
                            border-radius:8px;
                        ">

                            <h3 style="margin-top:0;">
                                Doctor Notes
                            </h3>

                            <p>
                                {notes}
                            </p>

                        </div>

                        <p style="margin-top:25px;">

                            We wish you a speedy recovery.

                        </p>

                        <p>

                            Thank you for choosing
                            <strong>Safe Care Hospital</strong>.

                        </p>

                    </div>

                    <!-- FOOTER -->

                    <div style="
                        background:#212529;
                        color:white;
                        text-align:center;
                        padding:20px;
                    ">

                        <h3 style="margin:0;">
                            Safe Care Hospital
                        </h3>

                        <p style="margin-top:8px;">
                            Advanced Healthcare Management System
                        </p>

                        <p style="margin-top:8px;">
                            Email: safecarehospital236@gmail.com
                        </p>

                    </div>

                </div>

            </body>
            </html>
            """

            email = EmailMultiAlternatives(

                subject,

                "Prescription Details",

                settings.DEFAULT_FROM_EMAIL,

                [patient_email]

            )

            email.attach_alternative(
                html_content,
                "text/html"
            )

            email.send()

        except Exception as e:

            print("EMAIL ERROR:", str(e))

        # =========================================
        # RESPONSE
        # =========================================

        if created:

            return Response(
                {
                    "message":
                    "Prescription Added Successfully and Email Sent"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message":
                "Prescription Updated Successfully and Email Sent"
            },
            status=status.HTTP_200_OK
        )


class PrescriptionPDFAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        try:

            prescription = Prescription.objects.get(
                id=pk
            )

        except Prescription.DoesNotExist:

            return Response(
                {
                    "error": "Prescription not found"
                },
                status=404
            )

        response = HttpResponse(
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="Prescription_{pk}.pdf"'

        p = canvas.Canvas(response)

        p.setFont(
            "Helvetica-Bold",
            18
        )

        p.drawString(
            180,
            800,
            "SAFE CARE HOSPITAL"
        )

        p.setFont(
            "Helvetica",
            12
        )

        p.drawString(
            50,
            740,
            f"Prescription ID : {prescription.id}"
        )

        p.drawString(
            50,
            710,
            f"Date : {prescription.created_at.strftime('%d-%m-%Y')}"
        )

        p.drawString(
            50,
            680,
            f"Patient : {prescription.appointment.patient.user.get_full_name()}"
        )

        p.drawString(
            50,
            650,
            f"Doctor : {prescription.appointment.doctor.user.get_full_name()}"
        )

        p.drawString(
            50,
            600,
            "Diagnosis :"
        )

        p.drawString(
            150,
            600,
            prescription.diagnosis
        )

        p.drawString(
            50,
            550,
            "Medicines :"
        )

        p.drawString(
            150,
            550,
            prescription.medicines
        )

        p.drawString(
            50,
            500,
            "Notes :"
        )

        p.drawString(
            150,
            500,
            prescription.notes
        )

        p.drawString(
            50,
            420,
            "Get Well Soon!"
        )

        p.save()

        return response
            

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
    
