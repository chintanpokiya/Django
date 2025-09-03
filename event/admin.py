from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

# Define an inline admin descriptor for Profile model
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False  # Optional, you can set this to True if you'd like

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInLine]  # Add the Profile as inline form
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]  # Add fields for display

# Unregister the original User admin and register the custom one
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)

