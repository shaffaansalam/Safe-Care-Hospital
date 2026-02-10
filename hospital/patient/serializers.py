from rest_framework import serializers
from django.contrib.auth.models import User
# IMPORT FROM AUTHENTICATION APP, NOT FROM .models
from authentication.models import UserProfile ,PatientProfile,DoctorProfile


# class UserRegSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'first_name', 'last_name']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)

class UserRegSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES, write_only=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password',
            'first_name', 'last_name', 'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role')

        user = User.objects.create_user(**validated_data)

        UserProfile.objects.create(user=user, role=role)

        if role == 'patient':
            PatientProfile.objects.create(
                user=user,
                phone='',
                gender='other',
                dob='2000-01-01',
                age=0,
                address='',
                blood_group=''
            )

        elif role == 'doctor':
            DoctorProfile.objects.create(
                user=user,
                phone='',
                specialization='',
                qualification='',
                experience=0,
                bio='',
                consultation_fee=0,
                available_start_time='09:00',
                available_end_time='17:00',
                is_approved=False
            )

        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserRegSerializer()

    class Meta:
        model = PatientProfile
        fields = [
            'user', 'phone', 'gender', 'dob', 'age', 
            'address', 'blood_group', 'medical_history'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        
        # Ensure you use the imported UserProfile from authentication
        UserProfile.objects.create(user=user, role='patient')

        patient_profile = PatientProfile.objects.create(user=user, **validated_data)
        return patient_profile