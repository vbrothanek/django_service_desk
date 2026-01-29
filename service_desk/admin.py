from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Company, User, Ticket, Record

@admin.register(Company)
class FirmAdmin(admin.ModelAdmin):
    list_display = ['name', 'ic', 'city', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'ic']



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('phone', 'companies')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional info', {'fields': ('phone', 'companies')}),
    )
    list_display = ('username', 'email', 'phone', 'is_staff')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'subject', 'user' ,'created_at', 'assigned_to']
    list_filter = ['ticket_number', 'created_at', 'assigned_to']
    search_fields = ['ticket_number', 'subject']

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'message']
    list_filter = ['ticket__ticket_number', 'message']