from django.contrib import admin
from users.models import Patient
from treatments.models import Feedback, Treatment, Prescription

admin.site.register(Feedback)
admin.site.register(Prescription)


class TreatmentInline(admin.TabularInline):
    model = Treatment
    extra = 1


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic', {'fields': ('doctor', 'patient')}),
        ('More Treatment Info', {
            "classes": ['collapse'],
            "fields": ['date', 'disease', 'remarks'],
        },
         ),
    )

