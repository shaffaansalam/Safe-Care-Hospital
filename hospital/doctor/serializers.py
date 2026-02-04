from rest_framework import serializers
from authentication.serializers import UserRegSerializer,UserProfile,DoctorProfile
# from authentication.models import *
from authentication.models import DoctorProfile
from django.contrib.auth.models import User
from .models import *

# class DoctorProfileSerializer(serializers.ModelSerializer):
#     user = UserRegSerializer()

#     class Meta:
#         model = DoctorProfile
#         fields = '__all__'

#     def create(self, validated_data):
        # user_data = validated_data.pop('user')
        # user = UserRegSerializer().create(user_data)

        # UserProfile.objects.create(user=user, role='doctor')

        # doctor = DoctorProfile.objects.create(user=user, **validated_data)
        # return doctor


 
# This handles the Doctor-specific fields
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = [
            'phone', 'specialization', 'qualification', 'experience', 
            'bio', 'consultation_fee', 'available_start_time', 
            'available_end_time'
        ]

# This handles the User creation and nests the Doctor data
class DoctorRegistrationSerializer(serializers.ModelSerializer):
    # This field MUST match the related_name='doctor' in your DoctorProfile model
    doctor = DoctorProfileSerializer()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 
            'first_name', 'last_name', 'doctor'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        # 1. Extract the nested doctor dictionary
        doctor_data = validated_data.pop('doctor')

        # 2. Create the User (hashes the password automatically)
        user = User.objects.create_user(**validated_data)

        # 3. Create the mandatory Base UserProfile
        UserProfile.objects.create(user=user, role='doctor')

        # 4. Create the DoctorProfile linked to this user
        DoctorProfile.objects.create(user=user, **doctor_data)

        return user
    
# request body format:: 
# {
#   "username": "dr_smith15",
#   "email": "smith@hospital.com",
#   "password": "securepassword123",
#   "first_name": "John",
#   "last_name": "Smith",
#   "doctor": {
#     "phone": "123456789012",
#     "specialization": "Cardiology",
#     "qualification": "MD, MBBS",
#     "experience": 10,
#     "bio": "Experienced cardiologist.",
#     "consultation_fee": "500.00",
#     "available_start_time": "09:00:00",
#     "available_end_time": "17:00:00"
#   }
# }