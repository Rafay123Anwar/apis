from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Only hash if not already hashed
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.email


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    # image = models.ImageField(upload_to='patient_images/', null=True, blank=True)
    image = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
