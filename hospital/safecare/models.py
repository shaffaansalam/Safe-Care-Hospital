

# class User(AbstractUser):
#     # We set username to None so it doesn't exist in the database
#     username = None 
#     email = models.EmailField(unique=True) # Email must be unique
#     name = models.CharField(max_length=150)
#     def __str__(self):
#         return self.email


# class UserProfile(models.Model):
#     ROLE_CHOICES = (
    
#         ('doctor', 'Doctor'),
#         ('patient', 'Patient'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.role}"

# class Patient(models.Model):
#     GENDER_CHOICES = (
#         ('male', 'Male'),
#         ('female', 'Female'),
#         ('other', 'Other'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=200)
#     phone = models.CharField(max_length=15)
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
#     dob = models.DateField()
#     age = models.PositiveIntegerField()
#     address = models.TextField()
#     blood_group = models.CharField(max_length=5, blank=True)
#     medical_history = models.TextField(blank=True)
#     profile_image = models.ImageField(upload_to='patients/', blank=True, null=True)

#     def __str__(self):
#         return self.full_name   
    



