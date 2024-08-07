from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView,TemplateView,DetailView,FormView,CreateView,DeleteView,UpdateView,View


class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = 'AMS/index.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        #Common context data
        context['Announcements'] = Announcement.objects.all()
        context['user'] = self.request.user
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
            context['DataForGrid'] = Doctor.objects.all()[:2]
            context['Treatment'] = Treatment.objects.filter(patient__user=user).first()
           

        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'
            context['DataForGrid'] = Patient.objects.all()[:2]
            context['Treatment'] = Treatment.objects.filter(doctor__user=user).first()
      
          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
            context['DataForGrid'] = Doctor.objects.all()[:2]
            
          
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
             # Get counts of Patients, Doctors, and Receptionists
            context['patient_count'] = Patient.objects.count()
            context['doctor_count'] = Doctor.objects.count()
            context['receptionist_count'] = CustomUser.objects.filter(groups__name='Receptionist').count()

        
        return context

#Log out user
def logout_user(request):
    logout(request)
    return redirect('login')  


class DoctorListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Doctor
    login_url = 'login'
    template_name = 'AMS/doctors.html'
    permission_required = 'AMS.view_doctor'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        # Common context data
        context['other_doctors'] = Doctor.objects.all()
        context['user'] = self.request.user
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
    

        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'

          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
           
          
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
            context['DataForGrid'] = Doctor.objects.all()[:2]
        
        return context


class SignupView(FormView):
    template_name = 'AMS/signup.html'
    form_class = SignupForm
    success_url = '/AMS'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)  # Redirect to a success page

    def form_invalid(self, form):
        # Render the form with errors
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(FormView):
    template_name = 'AMS/login.html'
    form_class = LoginForm
    success_url = '/AMS'

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)  # Authenticate using email and password

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)  # Redirect to a success page
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
  

class ReceptionistListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Receptionist
    login_url = 'login'
    template_name = 'AMS/receptionists.html'
    permission_required = 'AMS.view_receptionist'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #Common context data
        context['user'] = self.request.user
        context['receptionists'] = Receptionist.objects.all()
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
           
        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'
          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
            
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
        
        return context

# List View For Each patient's and doctor's all Appointments 
class AppointmentView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Appointment
    login_url = 'login'
    template_name = 'AMS/appointments.html'
    permission_required = 'AMS.view_appointment'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user'] = self.request.user
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
            context['Appointments'] = Appointment.objects.filter(patient__user = user).order_by('-appointment_date')
           
        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'
            context['Appointments'] = Appointment.objects.filter(doctor__user = user).order_by('-appointment_date')
          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
            context['Appointments'] = Appointment.objects.all()
           
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
            context['Appointments'] = Appointment.objects.all()
        
        return context
    

# List View For Each patient's and doctor's all Treatments 
class TreatmentView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name = 'AMS/treatments.html'
    login_url = 'login'
    model = Treatment
    permission_required = 'AMS.view_treatment'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['user'] = self.request.user
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
            context['Treatments'] = Treatment.objects.filter(patient__user = user).order_by('-date')
           
        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'
            context['Treatments'] = Treatment.objects.filter(doctor__user = user).order_by('-date')
          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
            context['Treatments'] = Treatment.objects.all()
           
          
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
            context['Treatments'] = Treatment.objects.all()
        
        return context
    

class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'AMS/patients.html'
    login_url = 'login'  # URL to redirect to if the user is not authenticated
    permission_required = 'AMS.view_patient'  # Permission required to access this view

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['user'] = self.request.user
        context['Patients'] = Patient.objects.all()
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Doctor').exists():
            doctor = user.doctor_profile
            # Filter patients who have appointments with this doctor
            context['my_patients'] = Patient.objects.filter(
                    id__in=Appointment.objects.filter(doctor=doctor).values_list('patient_id', flat=True)
                )
            context['role'] = 'Doctor'

        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
           
          
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
        
        return context

    
class PatientCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Patient
    login_url = 'login'
    form_class = PatientForm
    template_name = 'AMS/patient_form.html'
    success_url = reverse_lazy('patient_list')
    permission_required = 'AMS.add_patient'
    
        # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = CustomUserForm(self.request.POST, self.request.FILES)
        else:
            context['user_form'] = CustomUserForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid():
            self.object = form.save(commit=False)
            user = user_form.save()
            self.object.user = user
            self.object.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PatientUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Patient
    login_url = 'login'
    form_class = PatientForm
    template_name = 'AMS/patient_form.html'
    success_url = reverse_lazy('patient_list')
    permission_required = 'AMS.change_patient'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = CustomUserForm(self.request.POST, self.request.FILES, instance=self.object.user)
        else:
            context['user_form'] = CustomUserForm(instance=self.object.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid():
            user_form.save()
            form.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PatientDeleteView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Patient
    login_url = 'login'
    template_name = 'AMS/user_confirm_delete.html'
    success_url = reverse_lazy('patient_list')
    permission_required = 'AMS.delete_patient'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


class PatientDetailView(DetailView):
    model = Patient
    login_url = 'login'
    template_name = 'AMS/patient_detail.html'
    context_object_name = 'patient'


class DoctorCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Doctor
    login_url = 'login'
    form_class = DoctorForm
    template_name = 'AMS/doctor_form.html'
    success_url = reverse_lazy('doctor_list')
    permission_required = 'AMS.add_doctor'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = CustomUserForm(self.request.POST, self.request.FILES)
        else:
            context['user_form'] = CustomUserForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid():
            self.object = form.save(commit=False)
            user = user_form.save()
            self.object.user = user
            self.object.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class DoctorUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Doctor
    login_url = 'login'
    form_class = DoctorForm
    template_name = 'AMS/doctor_form.html'
    success_url = reverse_lazy('doctor_list')
    permission_required = 'AMS.change_doctor'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = CustomUserForm(self.request.POST, self.request.FILES, instance=self.object.user)
        else:
            context['user_form'] = CustomUserForm(instance=self.object.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid():
            user_form.save()
            form.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class DoctorDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Doctor
    login_url = 'login'
    template_name = 'AMS/user_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')
    permission_required = 'AMS.delete_doctor'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


class ReceptionistCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = CustomUser
    login_url = 'login'
    form_class = CustomUserForm
    template_name = 'AMS/receptionist_form.html'
    success_url = reverse_lazy('receptionist_list')
    permission_required = 'AMS.add_receptionist'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def form_valid(self, form):
        user = form.save()
        Receptionist.objects.create(user=user)
        return redirect(self.success_url)


class ReceptionistUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = CustomUser
    login_url = 'login'
    form_class = CustomUserForm
    template_name = 'AMS/receptionist_form.html'
    success_url = reverse_lazy('receptionist_list')
    permission_required = 'AMS.change_receptionist'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_object(self, queryset=None):
        receptionist = Receptionist.objects.get(pk=self.kwargs['pk'])
        return receptionist.user

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)


class ReceptionistDeleteView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    model = Receptionist
    login_url = 'login'
    template_name = 'AMS/user_confirm_delete.html'
    success_url = reverse_lazy('receptionist_list')
    permission_required = 'AMS.delete_receptionist'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_object(self, queryset=None):
        receptionist = Receptionist.objects.get(pk=self.kwargs['pk'])
        return receptionist.user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
    
class BookAppointmentView(LoginRequiredMixin,PermissionRequiredMixin, FormView):
    template_name = 'AMS/book_appointment.html'
    login_url = 'login'
    form_class = AppointmentForm
    permission_required = 'AMS.add_appointment'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diseases'] = Disease.objects.all()
        user = self.request.user

        # Determine the role of the user and add role-specific data
        if user.groups.filter(name='Admin').exists() or user.groups.filter(name='Receptionist').exists():
            context['patients'] = Patient.objects.all()
            context['role'] = 'Admin' if user.groups.filter(name='Admin').exists() else 'Receptionist'
        elif user.groups.filter(name='Patient').exists():
            if hasattr(user, 'patient_profile'):
                context['patients'] = [user.patient_profile]
            context['role'] = 'Patient'

        context['doctors'] = Doctor.objects.all()
        return context

    def form_valid(self, form):
        user = self.request.user

        # Determine the role of the user and assign the patient
        if user.groups.filter(name='Patient').exists():
            if hasattr(user, 'patient_profile'):
                form.instance.patient = user.patient_profile
            else:
                form.add_error(None, "Patient profile not found.")
                return self.form_invalid(form)

        if user.groups.filter(name='Admin').exists() or user.groups.filter(name='Receptionist').exists():
            patient_id = self.request.POST.get('patient')
            if patient_id:
                try:
                    form.instance.patient = Patient.objects.get(id=patient_id)
                except Patient.DoesNotExist:
                    form.add_error(None, "Selected patient does not exist.")
                    return self.form_invalid(form)
            else:
                form.add_error(None, "Patient must be selected.")
                return self.form_invalid(form)

        form.instance.status = Appointment.PENDING
        form.instance.doctor = form.cleaned_data['doctor']
        form.save()
        return redirect(reverse_lazy('appointment_list'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    

class UpdateAppointmentView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'AMS.change_appointment'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)
        
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if not (request.user.groups.filter(name='Receptionist').exists() or request.user.groups.filter(name='Admin').exists()):
            return redirect('forbidden')  # Redirect to forbidden page if unauthorized

        form = AppointmentForm(instance=appointment)
        return render(request, 'AMS/update_appointment.html', {'form': form, 'appointment': appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if not (request.user.groups.filter(name='Receptionist').exists() or request.user.groups.filter(name='Admin').exists()):
            return redirect('login')  # Redirect to login page if unauthorized

        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
        return render(request, 'AMS/update_appointment.html', {'form': form, 'appointment': appointment})


class CancelAppointmentView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'AMS.delete_appointment'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)
        
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if (request.user.groups.filter(name='Doctor').exists()):
            return redirect('login')  # Redirect to login page if unauthorized

        appointment.status = Appointment.CANCELLED  # Assuming you have a CANCELLED status
        appointment.save()
        return redirect('appointment_list')
    

class AnnouncementListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model = Announcement
    login_url = 'login'
    template_name = 'AMS/announcements.html'
    permission_required = 'AMS.view_announcement'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['user'] = self.request.user
        context['announcements'] = Announcement.objects.all()
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'

        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
          
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'

        elif user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
        
        return context


class AnnouncementDetailView(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    model = Announcement
    login_url = 'login'
    template_name = 'AMS/announcement_detail.html'
    context_object_name = 'announcement'
    permission_required = 'AMS.view_announcement'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


class AnnouncementCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Announcement
    login_url = 'login'
    form_class = AnnouncementForm
    template_name = 'AMS/announcement_form.html'
    success_url = reverse_lazy('announcement_list')
    permission_required = 'AMS.add_announcement'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Announcement
    login_url = 'login'
    fields = ['title', 'description']
    template_name = 'AMS/announcement_form.html'
    success_url = reverse_lazy('announcement_list')
    permission_required = 'AMS.change_announcement'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


class AnnouncementDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Announcement
    login_url = 'login'
    template_name = 'AMS/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcement_list')
    permission_required = 'AMS.delete_announcement'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


class TreatmentCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Treatment
    login_url = 'login'
    form_class = TreatmentForm
    template_name = 'AMS/treatment_form.html'
    success_url = reverse_lazy('treatment_list')
    permission_required = 'AMS.add_treatment'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['prescription_form'] = PrescriptionForm(self.request.POST)
        else:
            context['prescription_form'] = PrescriptionForm()
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the logged-in user to the form
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        prescription_form = context['prescription_form']
        if prescription_form.is_valid():
            # Save the treatment form
            self.object = form.save()
            # Save the prescription form with the treatment
            prescription = prescription_form.save(commit=False)
            prescription.treatment = self.object
            prescription.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class TreatmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    model = Treatment
    login_url = 'login'
    form_class = TreatmentForm
    template_name = 'AMS/treatment_form.html'
    success_url = reverse_lazy('treatment_list')
    permission_required = 'AMS.change_treatment'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['prescription_form'] = PrescriptionForm(self.request.POST, instance=self.object.prescriptions)
        else:
            context['prescription_form'] = PrescriptionForm(instance=self.object.prescriptions)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        prescription_form = context['prescription_form']
        if prescription_form.is_valid():
            self.object = form.save()
            # Save or update the prescription form with the treatment
            prescription = prescription_form.save(commit=False)
            prescription.treatment = self.object
            prescription.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Override get_object to handle the correct Treatment object
        obj = super().get_object(queryset)
        # Prepopulate the prescription form with the existing prescription
        if not hasattr(obj, 'prescriptions'):
            # Create an empty Prescription if none exists
            Prescription.objects.create(treatment=obj)
        return obj
    

class DiseaseCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Disease
    login_url = 'login'
    fields = ['name', 'description']
    template_name = 'AMS/disease_form.html'
    success_url = reverse_lazy('disease_list')
    permission_required = 'AMS.add_disease'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def form_valid(self, form):
        if self.request.user.groups.first().name != 'Admin':
            return self.handle_no_permission()
        return super().form_valid(form)


class DiseaseUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Disease
    login_url = 'login'
    fields = ['name', 'description']
    template_name = 'AMS/disease_form.html'
    success_url = reverse_lazy('disease_list')
    permission_required = 'AMS.change_disease'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def form_valid(self, form):
        #checking the permissions
        if self.request.user.groups.first().name != 'Admin':
            return self.handle_no_permission()
        return super().form_valid(form)


class DiseaseDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Disease
    login_url = 'login'
    template_name = 'AMS/disease_confirm_delete.html'
    success_url = reverse_lazy('disease_list')
    permission_required = 'AMS.delete_disease'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def form_valid(self, form):
        if self.request.user.groups.first().name != 'Admin':
            return self.handle_no_permission()
        return super().form_valid(form)
    

class DiseaseListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model = Disease
    login_url = 'login'
    template_name = 'AMS/disease_list.html'
    context_object_name = 'diseases'
    permission_required = 'AMS.view_disease'
    
     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # setting user role according to logged user
        user_role = self.request.user.groups.first().name 
        context['role'] = user_role
        return context
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    login_url = 'login'
    form_class = EditProfileForm
    template_name = 'AMS/edit_profile.html'
    success_url = reverse_lazy('index')  

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        # Return the user instance to be edited
        return self.request.user
    
class FeedbackFormView(LoginRequiredMixin,PermissionRequiredMixin,FormView):
    form_class = FeedbackForm
    login_url ='login'
    template_name = 'AMS/feedback.html'
    success_url = reverse_lazy('treatment_list')
    permission_required = 'AMS.add_feedback'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        treatment_id = self.kwargs['treatment_id']
        context['treatment'] = get_object_or_404(Treatment, id=treatment_id)
        return context

    def form_valid(self, form):
        treatment_id = self.kwargs['treatment_id']
        treatment = get_object_or_404(Treatment, id=treatment_id)

        # setting treatment id and user manually from the logged in user
        form.instance.treatment = treatment
        form.instance.patient = self.request.user.patient_profile 

        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
