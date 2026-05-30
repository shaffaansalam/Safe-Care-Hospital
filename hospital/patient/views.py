# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from doctor.serializers import *
from patient.serializers import *
from django.db import IntegrityError
from authentication.models import Prescription,MedicalReport,TestRequest
from .serializers import PrescriptionSerializer,MedicalReportSerializer




class PatientDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.profile.role != "patient":
            return Response({"error": "Unauthorized"}, status=403)

        patient = request.user.patient
        serializer = PatientDashboardSerializer(patient, context={'request': request})
        return Response(serializer.data, status=200)
    


class BookAppointmentAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        if request.user.profile.role != "patient":
            return Response(
                {"error": "Only patients can book appointments"},
                status=403
            )

        serializer = AppointmentSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():

            try:
                appointment = serializer.save()



                return Response({

                   "message": "Appointment booked successfully",

                   "appointment": {
                   "id": appointment.id,
                   "doctor": appointment.doctor.user.get_full_name(),
                   "date": appointment.appointment_date,
                   "time": appointment.appointment_time,
                   "status": appointment.status
                    }

               }, status=201)

            except IntegrityError:
                return Response({
                    "error": "This appointment slot is already booked"
                }, status=400)

        return Response(serializer.errors, status=400)
            


class PatientAppointmentsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if not hasattr(request.user, 'patient'):
            return Response({"error": "Only patients allowed"}, status=403)

        appointments = Appointment.objects.filter(
            patient=request.user.patient
        ).select_related("doctor")

        serializer = AppointmentSerializer(appointments, many=True)

        return Response(serializer.data)
    

    # =========================================
# PATIENT PRESCRIPTIONS
# =========================================

class PatientPrescriptionsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.profile.role != "patient":

            return Response(
                {"error": "Only patients allowed"},
                status=403
            )

        prescriptions = Prescription.objects.filter(
            appointment__patient=request.user.patient
        )

        serializer = PrescriptionSerializer(
            prescriptions,
            many=True
        )

        return Response(serializer.data)
    
    # =========================================
# PATIENT REPORTS
# =========================================

class PatientReportsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.profile.role != "patient":

            return Response(
                {"error": "Only patients allowed"},
                status=403
            )

        reports = MedicalReport.objects.filter(
            patient=request.user.patient
        )

        serializer = MedicalReportSerializer(
            reports,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
    

class RequestMedicalTestAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, appointment_id):

        # ONLY DOCTOR
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

        test_name = request.data.get("test_name")

        instructions = request.data.get("instructions")



        # UPDATE IF EXISTS
        test_request, created = TestRequest.objects.update_or_create(

            appointment=appointment,

            defaults={

                "test_name": test_name,

                "instructions": instructions,

                "status": "pending"
            }
        )



        if created:

            return Response({

                "message": "Test requested successfully",

                "data": TestRequestSerializer(test_request).data

            }, status=201)



        return Response({

            "message": "Test request updated successfully",

            "data": TestRequestSerializer(test_request).data

        }, status=200)
    
class PatientUploadReportAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, test_request_id):

        # ONLY PATIENT
        if request.user.profile.role != "patient":

            return Response(
                {"error": "Only patients allowed"},
                status=403
            )

        try:

            test_request = TestRequest.objects.get(
                id=test_request_id,
                appointment__patient=request.user.patient
            )

        except TestRequest.DoesNotExist:

            return Response(
                {"error": "Test request not found"},
                status=404
            )

        serializer = MedicalReportSerializer(
            data=request.data
        )

        if serializer.is_valid():

            report = serializer.save(
                test_request=test_request,
                patient=request.user.patient,
                doctor=test_request.appointment.doctor
            )

            # ==========================
            # AUTO COMPLETE TEST REQUEST
            # ==========================

            test_request.status = "completed"

            test_request.save()

            return Response({
                "message": "Report uploaded successfully",
                "data": serializer.data
            }, status=201)

        return Response(
            serializer.errors,
            status=400
        )


          

 # =========================================
# PATIENT TEST REQUESTS
# =========================================

class PatientTestRequestsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.profile.role != "patient":

            return Response(
                {"error": "Only patients allowed"},
                status=403
            )

        tests = TestRequest.objects.filter(
            appointment__patient=request.user.patient
        )

        serializer = TestRequestSerializer(
            tests,
            many=True
        )

        return Response(serializer.data)

