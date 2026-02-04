from authentication.models import *
from rest_framework import serializers
from authentication.serializers import UserRegSerializer


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserRegSerializer()

    class Meta:
        model = PatientProfile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserRegSerializer().create(user_data)

        UserProfile.objects.create(user=user, role='patient')

        patient = PatientProfile.objects.create(user=user, **validated_data)
        return patient


