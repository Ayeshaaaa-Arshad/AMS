from appointments.models import Appointment
from django.contrib import admin
from appointments.constants import CANCELLED


def cancel_appointment(modeladmin, request, queryset):
    queryset.update(status=CANCELLED)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    date_hierarchy = 'appointment_date'

    fields = ['updated_by', ('patient', 'disease'), 'doctor', ('appointment_date', 'status')]
    list_select_related = ['patient', 'doctor']
    ordering = ['appointment_date']
    raw_id_fields = ["patient"]
    actions = [cancel_appointment]
