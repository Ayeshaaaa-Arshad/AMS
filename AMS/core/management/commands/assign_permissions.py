from core.models import Disease 
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
 

class Command(BaseCommand):
    help = 'Assign built-in permissions to admin for disease model'

    def handle(self, *args, **options):
        
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # Get the ContentType for the Disease model
        content_type = ContentType.objects.get_for_model(Disease)

        # Define the built-in permissions
        permissions = [
            'add_disease',
            'change_disease',
            'delete_disease',
            'view_disease',
        ]

        # Get the permissions and assign them to the Admin group
        for codename in permissions:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            admin_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions to Admin group'))
