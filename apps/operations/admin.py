from django.contrib import admin

# project imports
from apps.operations.models import TrainingForm, NotificationTemplate
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from apps.operations.models.user import User


@admin.register(TrainingForm)
class ContactModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id", 
        "full_name", 
        "email_id", 
        "phone_number", 
        "interested_in_training"
    )
    
    list_filter = (
        "id",
        "interested_in_training"
    )
    
    search_fields = (
        "full_name", 
        "email_id", 
        "phone_number"
    )


@admin.register(NotificationTemplate)
class NotificationTemplateModelAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "name",
        "subject",
        "content",
        "create_date",
        "modified_date",
    )
    
    search_fields = (
        "name", 
        "subject", 
        "content",
        "phone_number", 
        "intrested_in_training"
    )

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "name", "phone")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "phone", "otp", "classroom_link")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", "user_type")},
        ),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )
    readonly_fields = ("date_joined",)
