from django.contrib import admin

from user.models import User
from django.contrib.auth.admin import UserAdmin

from django.contrib.sessions.models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "name",
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "email",
                        "name",
                        "avatar",
                        "is_staff",
                        "is_active",
                        "is_email_verified",
                        "password1",
                        "password2",
                    )
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "email",
                        "name",
                        "avatar",
                        "is_staff",
                        "is_active",
                        "is_email_verified",
                        "password",
                    )
                ),
            },
        ),
    )
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
