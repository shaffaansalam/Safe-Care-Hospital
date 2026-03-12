from rest_framework import serializers
from django.contrib.auth.models import User
# IMPORT FROM AUTHENTICATION APP, NOT FROM .models
from authentication.models import UserProfile ,PatientProfile,DoctorProfile,Appointment,Department

class UserRegSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES, write_only=True
    )

    # Patient fields
    phone = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    dob = serializers.DateField(required=False, allow_null=True)
    blood_group = serializers.CharField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)

    # Doctor fields  ⭐ ADD THESE
    specialization = serializers.CharField(required=False)
    qualification = serializers.CharField(required=False)
    experience = serializers.IntegerField(required=False)
    consultation_fee = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False
    )
    bio = serializers.CharField(required=False, allow_blank=True)
    available_start_time = serializers.TimeField(required=False, allow_null=True)
    available_end_time = serializers.TimeField(required=False, allow_null=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(),
    required=False,allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password',
            'first_name', 'last_name', 'role',

            # patient
            'phone', 'gender', 'dob', 'blood_group', 'address',

            # doctor
            'specialization', 'qualification',
            'experience', 'consultation_fee',
            'bio', 'available_start_time', 'available_end_time','department'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        role = validated_data.pop('role').lower()

        # Patient fields
        phone = validated_data.pop('phone', '')
        gender = validated_data.pop('gender', 'other')
        dob = validated_data.pop('dob', None)
        blood_group = validated_data.pop('blood_group', '')
        address = validated_data.pop("address", '')

        # Doctor fields
        specialization = validated_data.pop('specialization', '')
        qualification = validated_data.pop('qualification', '')
        experience = validated_data.pop('experience', 0)
        consultation_fee = validated_data.pop('consultation_fee', 0)
        bio = validated_data.pop('bio', '')
        available_start_time = validated_data.pop('available_start_time', None)
        available_end_time = validated_data.pop('available_end_time', None)
        department = validated_data.pop('department', None)

        # Create user
        user = User.objects.create_user(**validated_data)

        # Create role profile
        UserProfile.objects.create(
            user=user,
            role=role
        )

        # PATIENT PROFILE
        if role == 'patient':

            PatientProfile.objects.create(
                user=user,
                phone=phone,
                gender=gender,
                dob=dob,
                blood_group=blood_group,
                address=address
            )

        # DOCTOR PROFILE
        if role == 'doctor':

            DoctorProfile.objects.create(
                
                user=user,
                phone=phone,
                specialization=specialization,
                qualification=qualification,
                experience=experience,
                consultation_fee=consultation_fee,
                bio=bio,
                available_start_time=available_start_time,
                available_end_time=available_end_time,
                department=department,
                is_approved=False
            )
            print("Doctor profile created for:", user.email)

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

class PatientDashboardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
        fields = [
            'user',
            'phone',
            'gender',
            'dob',
            'age',
            'address',
            'blood_group',
            'medical_history',
            'profile_image'
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.get_full_name(),
            "email": obj.user.email,
            "role": obj.user.profile.role
        } 
       
    

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):

        doctor = data['doctor']
        date = data['appointment_date']
        time = data['appointment_time']

        conflict = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            appointment_time=time,
            status__in=['pending','accepted']
        ).exists()

        if conflict:
            raise serializers.ValidationError(
                "Doctor already has an appointment at this time"
            )

        return data       