from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Patient, Doctor, Receptionist, CustomUser
from treatments.admin import TreatmentInline


# Customizing Admin Panel to see Users with more fields
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Basic', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'gender'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_display_links = ['first_name','email']
    list_editable = ['is_staff']
    list_filter = ['first_name', 'last_name']
    list_per_page = 5
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# Making Patient Admin customized view for displaying Table name Patient instead of User because it is inherited from
# User
class PatientAdmin(admin.ModelAdmin):
    verbose_name = "Patient"
    verbose_name_plural = "Patients"
    inlines = [TreatmentInline]
    save_on_top = True


# Making Doctor Admin customized view for displaying Table name Patient instead of User because it is inherited from
# User
class DoctorAdmin(admin.ModelAdmin):
    verbose_name = "Doctor"
    verbose_name_plural = "Doctors"


# Registering Rest of the Models
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
