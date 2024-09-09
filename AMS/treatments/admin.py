from datetime import date
from django.contrib import admin
from treatments.models import Feedback, Treatment, Prescription


admin.site.register(Feedback)
admin.site.register(Prescription)


class TreatmentYearListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Years"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "year"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("2010-2020", "From 2010 to 2020"),
            ("2020-2030", "From 2020 to 2030"),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == "2010-2020":
            return queryset.filter(
                date__gte=date(2010, 1, 1),
                date__lte=date(2020, 12, 31),
            )
        if self.value() == "2020-2030":
            return queryset.filter(
                date__gt=date(2020, 1, 1),
                date__lte=date(2030, 12, 31),
            )


class AdvancedTreatmentYearListFilter(TreatmentYearListFilter):
    def lookups(self, request, model_admin):
        """
        Only show the lookups if there actually is
        anyone have treatment in the corresponding years.
        """
        qs = model_admin.get_queryset(request)
        if qs.filter(
                date__gte=date(2010, 1, 1),
                date__lte=date(2020, 12, 31),
        ).exists():
            yield "2010-2020", "From 2010 to 2020"
        if qs.filter(
                date__gt=date(2020, 1, 1),
                date__lte=date(2030, 12, 31),
        ).exists():
            yield "2020-2030", "From 2020 to 2030"



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
    list_filter = [AdvancedTreatmentYearListFilter,
                   ("doctor", admin.RelatedOnlyFieldListFilter),
                   ("remarks", admin.EmptyFieldListFilter),
                   ]
