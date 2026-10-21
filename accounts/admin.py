from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Django's ready-made admin page for users

from .models import User  # Our custom User from models.py


@admin.register(User)  # Show our User model in the /admin panel
class CustomUserAdmin(UserAdmin):
    # Admin page for users. Same as Django's default, plus the role field.

    # Add a "Footprint" section with the role field to the user edit page
    fieldsets = UserAdmin.fieldsets + (("Footprint", {"fields": ("role",)}),)

    # Columns shown in the list of users
    list_display = ("username", "email", "role", "is_staff")

    # Adds a "role" filter on the right side of the user list
    list_filter = UserAdmin.list_filter + ("role",)