from rest_framework import serializers
from authentication.serializers import UserProfile,DoctorProfile
from authentication.models import *
from django.contrib.auth.models import User



# This handles the Doctor-specific fields
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = [
            'phone', 'specialization', 'qualification', 'experience', 
            'bio', 'consultation_fee', 'available_start_time', 
            'available_end_time'
        ]

class DoctorRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    specialization = serializers.CharField()

    def create(self, validated_data):
        # 1️⃣ Create user but DISABLE login
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False   #  VERY IMPORTANT
        )

        # 2️⃣ Create doctor profile (NOT approved)
        DoctorProfile.objects.create(
            user=user,
            specialization=validated_data['specialization'],
            is_approved=False
        ) 

        UserProfile.objects.create(user=user, role='doctor')     

# class DoctorRegistrationSerializer(serializers.Serializer):

#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     specialization = serializers.CharField()
#     qualification = serializers.CharField()
#     experience = serializers.IntegerField()
#     consultation_fee = serializers.DecimalField(max_digits=8, decimal_places=2)

#     def create(self, validated_data):

#         user = User.objects.create_user(
#             username=validated_data["username"],
#             email=validated_data["email"],
#             password=validated_data["password"],
#             is_active=False
#         )

#         DoctorProfile.objects.create(
#             user=user,
#             specialization=validated_data["specialization"],
#             qualification=validated_data["qualification"],
#             experience=validated_data["experience"],
#             consultation_fee=validated_data["consultation_fee"],
#             is_approved=False
#         )

#         UserProfile.objects.create(
#             user=user,
#             role="doctor"
#         )

#         return user        


class DoctorDashboardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = [
            'user',
            'phone',
            'specialization',
            'qualification',
            'experience',
            'bio',
            'consultation_fee',
            'available_start_time',
            'available_end_time',
            'is_available',
            'profile_image'
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.get_full_name(),
            "email": obj.user.email,
            "role": obj.user.profile.role
        }


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


    


#     {
#   "message": "Doctor registered successfully",
#   "user": {
#     "id": 19,
#     "username": "dr_smith17",
#     "email": "smith@hospital.com",
#     "first_name": "John",
#     "last_name": "Smith",
#     "doctor": {
#       "phone": "123456789012",
#       "specialization": "Cardiology",
#       "qualification": "MD, MBBS",
#       "experience": 10,
#       "bio": "Experienced cardiologist.",
#       "consultation_fee": "500.00",
#       "available_start_time": "09:00:00",
#       "available_end_time": "17:00:00"
#     }
#   }
# }