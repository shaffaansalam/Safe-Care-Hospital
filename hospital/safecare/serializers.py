# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import UserProfile,PatientProfile,DoctorProfile
# from rest_framework.validators import UniqueValidator


# class UserSerializer(serializers.ModelSerializer):
#     role = serializers.CharField(source='profile.role', read_only=True)
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'last_login', 'role']


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     firstname = serializers.CharField(max_length=150)
#     role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='patient')
#     # email = serializers.EmailField(max_length=100, unique=True)
#     email = serializers.EmailField(
#         max_length=100,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(write_only=True, min_length=8)

#     class Meta:
#         model = User
#         fields = ['firstname', 'email', 'password','role']

#     def create(self, validated_data):
#         firstname = validated_data.pop('firstname')
#         role = validated_data.pop('role').lower()
#         user = User.objects.create_user(**validated_data)
#         UserProfile.objects.create(user=user, role=role)
#         return user
    

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='patient')
    
#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password', 'role']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         role = validated_data.pop('role').lower()
#         # create_user now only expects email, password, and name
#         user = User.objects.create_user(**validated_data)
#         UserProfile.objects.create(user=user, role=role)
#         return user
    

#         # # 2. Create the User object without the extra fields
#         # user = User.objects.create_user(
#         #     username=validated_data['username'],
#         #     email=validated_data['email'],
#         #     password=validated_data['password'],
#         #     first_name=name  # We save the 'name' into Django's 'first_name' field
#         # )

#         # # 3. Create the Profile linked to this user
#         # UserProfile.objects.create(user=user, role=role)
        
#         # return user


    
# class PatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Patient
#         fields = '__all__'

#     def validate_phone(self, value):
#         if not value.isdigit() or len(value) < 10:
#             raise serializers.ValidationError("Enter a valid phone number")
#         return value











