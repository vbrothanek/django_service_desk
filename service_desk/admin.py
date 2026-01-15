from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Firm, UserProfile, Ticket, Record

# Register your models here.
@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    list_display = ['name', 'ic', 'city', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'ic']



# UserProfileInline > To be able to edit UserProfile from user settings.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'subject', 'user' ,'created_at', 'assigned_to']
    list_filter = ['ticket_number', 'created_at', 'assigned_to']
    search_fields = ['ticket_number', 'subject']

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'description']
    list_filter = ['ticket__ticket_number', 'description']