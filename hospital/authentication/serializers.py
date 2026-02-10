from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate






# class UserRegSerializer(serializers.ModelSerializer):
#     role = serializers.ChoiceField(
#         choices=UserProfile.ROLE_CHOICES, write_only=True
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'role']
#         extra_kwargs = {
#             'password': {'write_only': True, 'min_length': 8},
#             'email': {'required': True}
#         }

#     def create(self, validated_data):
#         role = validated_data.pop('role')
      

#         # Create user
#         user = User.objects.create_user(**validated_data)

#         # Create base profile (MANDATORY)
#         UserProfile.objects.create(
#             user=user,
#             role=role
#         )

#         # Create role-specific profile
#         if role == 'patient':
#             PatientProfile.objects.create(
#                 user=user,
#                 phone='',
#                 gender='other',
#                 dob='2000-01-01',
#                 age=0,
#                 address='',
#                 blood_group='',
#             )

#         elif role == 'doctor':
#             DoctorProfile.objects.create(
#                 user=user,
#                 phone='',
#                 specialization='',
#                 qualification='',
#                 experience=0,
#                 bio='',
#                 consultation_fee=0,
#                 available_start_time='09:00',
#                 available_end_time='17:00',
#             )

#         return user



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         try:
#             user_obj = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("Invalid email or password")

#         user = authenticate(username=user_obj.username, password=password)

#         if not user:
#             raise serializers.ValidationError("Invalid email or password")

#         if not user.is_active:
#             raise serializers.ValidationError("User account is disabled")

#         attrs['user'] = user
#         return attrs
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        #  BLOCK DOCTOR LOGIN UNTIL APPROVED
        if user.profile.role == "doctor":
            if not user.doctorprofile.is_approved:
                raise serializers.ValidationError(
                    "Doctor account pending admin approval"
                )

        attrs['user'] = user
        return attrs





class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    # Logout usually doesn't need fields, but if using JWT, 
    # you might pass the 'refresh' token here to blacklist it.
    refresh = serializers.CharField()        

    