from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from doctor.serializers import *
from patient.serializers import *

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

        serializer = DoctorDashboardSerializer(doctor)
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
    
