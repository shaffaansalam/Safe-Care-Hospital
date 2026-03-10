from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
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
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=5)
    medical_history = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='patients/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
    def save(self, *args, **kwargs):

        if self.dob:
            today = date.today()

            self.age = today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )

        super().save(*args, **kwargs)

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor'
    )

    phone = models.CharField(max_length=12, blank=True, null=True)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)

    experience = models.PositiveIntegerField()
    bio = models.TextField(blank=True, null=True)

    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    available_start_time = models.TimeField(blank=True, null=True)
    available_end_time = models.TimeField(blank=True, null=True)

    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    profile_image = models.ImageField(upload_to='doctors/', blank=True, null=True)



class Appointment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    reason = models.TextField()

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"

class Payment(models.Model):

    PAYMENT_STATUS = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('failed', 'Failed'),
    )

    PAYMENT_METHOD = (
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('wallet', 'Wallet'),
    )

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD
    )

    transaction_id = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)      