# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from doctor.serializers import *
from patient.serializers import *
from django.db import IntegrityError


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