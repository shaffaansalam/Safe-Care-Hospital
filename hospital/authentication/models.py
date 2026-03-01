from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
# # Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='patient')

    def __str__(self):
        return f"{self.user.email} - {self.role}"


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')

    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField()
    address = models.TextField()
    blood_group = models.CharField(max_length=5)
    medical_history = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='patients/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()



class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='doctor'
    )

    phone = models.CharField(max_length=12)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    bio = models.TextField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    available_start_time = models.TimeField()
    available_end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False) # Admin must set this to True manually

    profile_image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


