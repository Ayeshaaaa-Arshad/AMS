from django.contrib import admin
from core.models import Disease,Announcement

#Registering Rest of the Models
admin.site.register(Disease)
admin.site.register(Announcement)
