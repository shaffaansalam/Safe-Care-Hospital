from rest_framework import serializers
from django.contrib.auth.models import User
# IMPORT FROM AUTHENTICATION APP, NOT FROM .models
from authentication.models import UserProfile ,PatientProfile,DoctorProfile,Appointment,Department,Prescription,MedicalReport,TestRequest
from datetime import datetime, date




class UserRegSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES, write_only=True
    )

    # Common fields for both profiles
    phone = serializers.CharField(required=False)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    # Patient fields
    gender = serializers.CharField(required=False)
    dob = serializers.DateField(required=False, allow_null=True)
    blood_group = serializers.CharField(required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    medical_history = serializers.CharField(required=False, allow_blank=True)
    age = serializers.IntegerField(required=False)
   

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
            'phone', 'gender', 'dob','age', 'blood_group', 'address','medical_history',
            'profile_image',
            

            # doctor
            'specialization', 'qualification',
            'experience', 'consultation_fee',
            'bio', 'available_start_time', 'available_end_time','department',
        
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        role = validated_data.pop('role').lower()

        # Extract the image ONCE
        profile_image = validated_data.pop('profile_image', None)
        phone = validated_data.pop('phone', '')

        # Patient fields
        
        gender = validated_data.pop('gender', 'other')
        dob = validated_data.pop('dob', None)
        blood_group = validated_data.pop('blood_group', '')
        address = validated_data.pop("address", '')
        medical_history = validated_data.pop("medical_history", '')
        age = validated_data.pop('age',None)
        

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
                address=address,
                medical_history=medical_history,
                age=age,
                profile_image=profile_image,
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
                is_approved=False,
                profile_image=profile_image,
            )
            print("Doctor profile created for:", user.email)

        return user

class SimpleUserSerializer(serializers.ModelSerializer):

    role=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email",'role',]

    def get_role(self,obj):
        return obj.profile.role        


class PatientProfileSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer()
    id = serializers.IntegerField(read_only=True)
   

    class Meta:
        model = PatientProfile
        fields = [
            'id','user', 'phone', 'gender', 'age', 
            'address', 'blood_group', 'medical_history',
            'profile_image',
        ]

    

class PatientDashboardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    profile_image = serializers.ImageField(read_only=True)

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
            'profile_image',
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.get_full_name(),
            "email": obj.user.email,
            "role": obj.user.profile.role
        } 
       
class PatientProfileUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = PatientProfile

        fields = [
            "phone",
            "gender",
            "dob",
            "blood_group",
            "address",
            "medical_history",
            "profile_image"
        ]


class AppointmentSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(
        source='doctor.user.get_full_name',
        read_only=True
    )

    patient_name = serializers.CharField(
        source='patient.user.get_full_name',
        read_only=True
    )

    patient_id = serializers.IntegerField(
        source='patient.id',
        read_only=True
    )

    patient_age = serializers.IntegerField(
        source='patient.age',
        read_only=True
    )

    patient_gender = serializers.CharField(
        source='patient.gender',
        read_only=True
    )

    patient_blood_group = serializers.CharField(
        source='patient.blood_group',
        read_only=True
    )

    medical_history = serializers.CharField(
        source='patient.medical_history',
        read_only=True
    )

    old_appointment_date = serializers.DateField(
    read_only=True
)

    old_appointment_time = serializers.TimeField(
    read_only=True
)

    rescheduled = serializers.BooleanField(
    read_only=True
)

    class Meta:
        model = Appointment

        fields = [

            'id',
            'doctor',
            'doctor_name',

            'patient_id',
            'patient_name',
            'patient_age',
            'patient_gender',
            'patient_blood_group',
            'medical_history',

            'appointment_date',
            'appointment_time',

            'requested_date',
            'requested_time',

            'rescheduled',
            'old_appointment_date',
            'old_appointment_time',

            'reason',
            'status',
            'created_at'
        ]

        read_only_fields = [
            'patient',
            'status'
        ]


    
    from authentication.models import Prescription, MedicalReport


# =========================================
# PRESCRIPTION SERIALIZER
# =========================================


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription

        fields = [
            "id",
            "appointment",
            "diagnosis",
            "medicines",
            "notes",
            "created_at"
        ]

        read_only_fields = [
            "appointment",
            "created_at"
        ]


# =========================================
# REPORT SERIALIZER
# =========================================

class MedicalReportSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='patient.user.get_full_name',
        read_only=True
    )

    doctor_name = serializers.CharField(
        source='doctor.user.get_full_name',
        read_only=True
    )

    class Meta:

        model = MedicalReport

        fields = [
            'id',
            'test_request',
            'patient',
            'doctor',
            'patient_name',
            'doctor_name',
            'report_title',
            'report_file',
            'uploaded_at'
        ]

        read_only_fields = [
            'test_request',
            'patient',
            'doctor',
            'patient_name',
            'doctor_name',
            'uploaded_at'
        ]

class TestRequestSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='appointment.patient.user.get_full_name',
        read_only=True
    )

    doctor_name = serializers.CharField(
        source='appointment.doctor.user.get_full_name',
        read_only=True
    )

    class Meta:

        model = TestRequest

        fields = [
            'id',
            'appointment',
            'patient_name',
            'doctor_name',
            'test_name',
            'instructions',
            'status',
            'requested_at'
        ]

        read_only_fields = [
            'appointment',
            'patient_name',
            'doctor_name',
            'requested_at'
        ]