from rest_framework import serializers
from authentication.models import DoctorProfile,Department
from django.contrib.auth.models import User



# This handles the Doctor-specific fields
class DoctorProfileSerializer(serializers.ModelSerializer):

    id =   serializers.IntegerField(read_only=True)
    user = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "user",
            "phone",
            "specialization",
            "qualification",
            "experience",
            "bio",
            "consultation_fee",
            "available_start_time",
            "available_end_time",
            "department",
            "profile_image",
            "is_approved",
        
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.get_full_name(),
            "email": obj.user.email,
            "role": obj.user.profile.role,
        }

    def get_department(self, obj):
        if obj.department:
            return obj.department.name
        return None
 
     


class DoctorDashboardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    department = serializers.CharField(source="department.name",read_only=True)
    profile_image = serializers.ImageField(read_only=True)

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
            'department',
            'available_start_time',
            'available_end_time',
            'is_available',
            'profile_image',
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.get_full_name(),
            "email": obj.user.email,
            "role": obj.user.profile.role
        }


class DoctorProfileUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = DoctorProfile

        fields = [

            "phone",

            "specialization",

            "qualification",

            "experience",

            "consultation_fee",

            "bio",

            "available_start_time",

            "available_end_time",

            "profile_image"
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"



# {
#   "username": "sachin_tendulkar",
#   "first_name": "sachin",
#   "last_name": "tendulkar",
#   "email": "sachin1234@gmail.com",
#   "password": "sachin4321",
#   "phone": "9447769634",
#   "role": "doctor",
#   "specialization": "Neurologist",
#   "qualification": "MBBS",
#   "experience": 10,
#   "bio": "Brain Specialist",
#   "consultation_fee": 300,
#   "available_start_time": "09:00:00",
#   "available_end_time": "17:00:00",
#   "department": 3
# }

# {
#   "message": "User registered successfully",
#   "user": {
#     "id": 175,
#     "username": "sachin_tendulkar",
#     "email": "sachin1234@gmail.com",
#     "role": "doctor"
#   }
# }

# {
#       "id": 87,
#       "user": {
#         "id": 175,
#         "name": "sachin tendulkar",
#         "email": "sachin1234@gmail.com",
#         "role": "doctor"
#       },
#       "phone": "9447769634",
#       "specialization": "Neurologist",
#       "qualification": "MBBS",
#       "experience": 10,
#       "bio": "Brain Specialist",
#       "consultation_fee": "300.00",
#       "available_start_time": "09:00:00",
#       "available_end_time": "17:00:00",
#       "department": "Neurology",
#       "is_approved": false
#     }
# {
#   "message": "Doctor approved successfully"
# }