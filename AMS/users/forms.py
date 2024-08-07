
from django import forms
from treatments.forms import *
from django.contrib.auth.models import Group
from .models import CustomUser,Patient,Doctor
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Signup Form inherited from UserCreationForm as we want to add some extra fields 
class SignupForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name","last_name", "password1", "password2")

# Login Form inherited from AuthenticationForm as we want to add some extra fields 
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = get_user_model()
        fields = ("username", "password")


#CustomUserForm
class CustomUserForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=[
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Receptionist', 'Receptionist')
    ], required=True)
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email', 'gender','image', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Hash the password
        if commit:
            user.save()

             # Assign user to the selected group
            user_type = self.cleaned_data.get('user_type')
            group = Group.objects.get(name=user_type)
            user.groups.add(group)
        return user

#Patient Form
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age']

#Doctor Form
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['designation']


#EditProfileForm with custom fields
class EditProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image']

    def __init__(self, *args, **kwargs):
        # Extract the user object from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # role-specific fields if the user is a patient, doctor, 
        if user:
            if user.groups.filter(name='Patient').exists():
                self.fields['age'] = forms.IntegerField(
                    initial=user.patient_profile.age,
                    widget=forms.NumberInput(attrs={'placeholder': 'Age'})
                )
            elif user.groups.filter(name='Doctor').exists():
                self.fields['designation'] = forms.CharField(
                    initial=user.doctor_profile.designation,
                    widget=forms.TextInput(attrs={'placeholder': 'Designation'})
                )

    def save(self, commit=True):
        user = super().save(commit=False)
        # Save custom fields
        if commit:
            user.save()
        # Update role-specific details if applicable
        if user.groups.filter(name='Patient').exists():
            patient = user.patient_profile
            if 'age' in self.cleaned_data:
                patient.age = self.cleaned_data['age']
                patient.save()
        elif user.groups.filter(name='Doctor').exists():
            doctor = user.doctor_profile
            if 'designation' in self.cleaned_data:
                doctor.designation = self.cleaned_data['designation']
                doctor.save()
       
        return user
    