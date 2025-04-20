from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "user_type", "is_staff")
    list_filter = ("user_type", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Info", {"fields": ("phone", "user_type")}),
        ("Permissions", {"fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type", "is_staff"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
