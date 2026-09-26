from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("role",)
    fieldsets = UserAdmin.fieldsets + (("Роль на порталі", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Роль на порталі", {"fields": ("role",)}),)
