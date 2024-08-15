from django.contrib import admin
from core.models import Disease, Announcement

# Registering Rest of the Models
admin.site.register(Disease)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['creator', 'title', 'is_deleted']
