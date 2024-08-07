
from django import forms
from users.models import *
from django.utils import timezone
from .models import Appointment

#AppointmentForm
class AppointmentForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor','status', 'disease', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'disease': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.groups.filter(name='Patient').exists():
                self.fields['patient'].queryset = Patient.objects.filter(user=user)
                self.fields['patient'].initial = user.patient_profile
                self.fields['doctor'].queryset = Doctor.objects.all()
                
            elif user.groups.filter(name='Admin').exists() or user.groups.filter(name='Receptionist').exists():
                self.fields['patient'].queryset = Patient.objects.all()
                self.fields['doctor'].queryset = Doctor.objects.all()
            else:
                # Non-admin and non-doctor users see no patients and doctors
                self.fields['patient'].queryset = Patient.objects.none()
                self.fields['doctor'].queryset = Doctor.objects.none()

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        now = timezone.now()

        if appointment_date and appointment_date < now:
            self.add_error('appointment_date', "The appointment date cannot be in the past.")

        return appointment_date
    