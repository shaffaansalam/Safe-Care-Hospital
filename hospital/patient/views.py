# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from doctor.serializers import *
from patient.serializers import *
from django.db import IntegrityError
from authentication.models import Prescription
from authentication.models import MedicalReport

from .serializers import PrescriptionSerializer
from .serializers import MedicalReportSerializer



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
    
# class UploadMedicalReportAPIView(APIView):

#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, patient_id):

#         if request.user.profile.role != "doctor":

#             return Response(
#                 {"error": "Only doctors allowed"},
#                 status=403
#             )

#         try:
#             patient = PatientProfile.objects.get(
#                 id=patient_id
#             )

#         except PatientProfile.DoesNotExist:

#             return Response(
#                 {"error": "Patient not found"},
#                 status=404
#             )

#         serializer = MedicalReportSerializer(
#             data=request.data,
#             context={'request': request}
#         )

#         if serializer.is_valid():

#             serializer.save(
#                 patient=patient,
#                 doctor=request.user.doctor
#             )

#             return Response({
#                 "message": "Report uploaded successfully",
#                 "data": serializer.data
#             })

#         return Response(
#             serializer.errors,
#             status=400
#         )
class RequestMedicalTestAPIView(APIView):

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

        serializer = TestRequestSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                appointment=appointment,
                doctor=request.user.doctor,
                patient=appointment.patient
            )

            return Response({
                "message": "Test requested successfully",
                "data": serializer.data
            })

        return Response(
            serializer.errors,
            status=400
        )
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

            serializer.save(

                test_request=test_request,

                patient=request.user.patient,

                doctor=test_request.appointment.doctor
            )

            return Response({

                "message": "Report uploaded successfully",

                "data": serializer.data

            }, status=201)

        return Response(
            serializer.errors,
            status=400
        )