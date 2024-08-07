from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect ,redirect , HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView,TemplateView,DetailView,FormView,CreateView,DeleteView,UpdateView


#Log out user
def logout_user(request):
    logout(request)
    return redirect('users:login')  


class SignupView(FormView):
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)  # Redirect to a success page

    def form_invalid(self, form):
        # Render the form with errors
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:index')

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


class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'users/patients.html'
    login_url = reverse_lazy('users:login') # URL to redirect to if the user is not authenticated
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
    login_url = reverse_lazy('users:login')
    form_class = PatientForm
    template_name = 'users/patient_form.html'
    success_url = reverse_lazy('users:patient_list')
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
    login_url = reverse_lazy('users:login')
    form_class = PatientForm
    template_name = 'users/patient_form.html'
    success_url = reverse_lazy('users:patient_list')
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
    login_url = reverse_lazy('users:login')
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:patient_list')
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
    login_url = reverse_lazy('users:login')
    template_name = 'users/patient_detail.html'
    context_object_name = 'patient'


class DoctorListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Doctor
    login_url = reverse_lazy('users:login')
    template_name = 'users/doctors.html'
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
    

class DoctorCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Doctor
    login_url = reverse_lazy('users:login')
    form_class = DoctorForm
    template_name = 'users/doctor_form.html'
    success_url = reverse_lazy('users:doctor_list')
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
    login_url = reverse_lazy('users:login')
    form_class = DoctorForm
    template_name = 'users/doctor_form.html'
    success_url = reverse_lazy('users:doctor_list')
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
    login_url = reverse_lazy('users:login')
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:doctor_list')
    permission_required = 'AMS.delete_doctor'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


class ReceptionistListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Receptionist
    login_url = reverse_lazy('users:login')
    template_name = 'users/receptionists.html'
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
    

class ReceptionistCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = CustomUser
    login_url = reverse_lazy('users:login')
    form_class = CustomUserForm
    template_name = 'users/receptionist_form.html'
    success_url = reverse_lazy('users:receptionist_list')
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
    login_url = reverse_lazy('users:login')
    form_class = CustomUserForm
    template_name = 'users/receptionist_form.html'
    success_url = reverse_lazy('users:receptionist_list')
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
    login_url = reverse_lazy('usesr:login')
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:receptionist_list')
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
      

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    login_url = reverse_lazy('users:login')
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('core:index')  

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        # Return the user instance to be edited
        return self.request.user
    