from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    models        = NewUser
    search_fields = ("email", "user_name")
    list_filter   = ("email", "user_name", "is_active", "is_staff")
    ordering      = ("-start_date",)
    list_display  = ("email", "id", "user_name", "auth_provider", "is_active", "is_staff")
    fieldsets     = (
        (None, {
            "fields": ("email", "user_name", "auth_provider")
        }),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "user_name", "password", "is_active"),
        })
    )

admin.site.register(NewUser, UserAdminConfig)