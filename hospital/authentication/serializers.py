from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']
        


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

        if not user.is_active:
            raise serializers.ValidationError("Account is disabled")

        attrs['user'] = user
        return attrs
    
    
class NotificationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Notification

        fields = [
            "id",
            "title",
            "message",
            "is_read",
            "created_at"
        ]    




class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    # Logout usually doesn't need fields, but if using JWT, 
    # you might pass the 'refresh' token here to blacklist it.
    refresh = serializers.CharField()        

    
class PaymentSerializer(
    serializers.ModelSerializer
):

    patient_name = serializers.CharField(
        source="patient.user.email",
        read_only=True
    )

    doctor_name = serializers.CharField(
        source="doctor.user.email",
        read_only=True
    )

    class Meta:

        model = Payment

        fields = "__all__" 