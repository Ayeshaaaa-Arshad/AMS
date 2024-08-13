from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin
from users.CustomManager import UserManager
from users.validators import validate_image_file_extension
from users.constants import GENDER_TYPE

class CustomUser(AbstractUser):

    class Meta:
        db_table = 'ams_customuser' 

    gender = models.CharField(max_length=1, choices=GENDER_TYPE)
    image = models.ImageField(upload_to='profile/images', verbose_name='Profile Image', blank=True, null=True, validators=[validate_image_file_extension])
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'  # setting Email for log in
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, related_name='patient_profile', on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        db_table = 'ams_patient' 

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}, Age: {self.age}"


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, related_name='doctor_profile', on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        db_table = 'ams_doctor' 

    def __str__(self):
        return f"Doctor: {self.user.first_name} {self.user.last_name}, Designation: {self.designation}"


class Receptionist(models.Model):
    user = models.OneToOneField(CustomUser, related_name='receptionist_profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Receptionist"
        verbose_name_plural = "Receptionists"
        db_table = 'ams_receptionist' 

    def __str__(self):
        return f"Receptionist: {self.user.first_name} {self.user.last_name}"

