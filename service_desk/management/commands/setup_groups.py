from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

'''
Django management command to create user groups for the Service Desk application.
This command creates three user groups in the database that are specified in groups list.
The command is idempotent - it can be run multiple times safely without creating duplicates.

Usage:
    python manage.py setup_groups
'''

class Command(BaseCommand):
    groups = ['Agents', 'Managers', 'Customers']

    help = f'Sets up the groups ({groups}) for service desk.'

    def handle(self, *args, **options):
        for group_name in self.groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group {group_name} already exists'))