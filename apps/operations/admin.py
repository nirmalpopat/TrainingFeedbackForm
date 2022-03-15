from django.contrib import admin

# project imports
from apps.operations.models import TrainingForm, NotificationTemplate
from import_export.admin import ImportExportModelAdmin

# Register your models here.

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
