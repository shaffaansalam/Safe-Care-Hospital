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
    medical_history = serializers.CharField(required=False, allow_blank=True)
    age = serializers.IntegerField(required=False)
    # profile_image = serializers.ImageField(required=False)

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
    profile_image = serializers.ImageField(required=False)
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
            # 'profile_image'
            

            # doctor
            'specialization', 'qualification',
            'experience', 'consultation_fee',
            'bio', 'available_start_time', 'available_end_time','department',
            # 'profile_image',
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
        medical_history = validated_data.pop("medical_history", '')
        age = validated_data.pop('age',None)
        # profile_image = validated_data.pop('profile_image',None)

        # Doctor fields
        specialization = validated_data.pop('specialization', '')
        qualification = validated_data.pop('qualification', '')
        experience = validated_data.pop('experience', 0)
        consultation_fee = validated_data.pop('consultation_fee', 0)
        bio = validated_data.pop('bio', '')
        available_start_time = validated_data.pop('available_start_time', None)
        available_end_time = validated_data.pop('available_end_time', None)
        department = validated_data.pop('department', None)
        # profile_image = validated_data.pop('profile_image',None)

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
                # profile_image=profile_image
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
                # profile_image=profile_image,
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
            # 'profile_image',
        ]

    

class PatientDashboardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # profile_image = serializers.ImageField(read_only=True)

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
            # 'profile_image',
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

        if doctor.available_start_time and doctor.available_end_time:
            if not (doctor.available_start_time <= time <= doctor.available_end_time):
              raise serializers.ValidationError(
                  "Appointment time is outside doctor's availability"
               )

        if conflict:
            raise serializers.ValidationError(
                "Doctor already has an appointment at this time"
            )

        return data       