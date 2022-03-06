from django.contrib import admin

# project imports
from apps.operations.models import TrainingInformations, NotificationTemplate
# Register your models here.

@admin.register(TrainingInformations)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "full_name", 
        "email_id", 
        "phone_number", 
        "intrested_in_training"
    )
    
    list_filter = (
        "id", 
        "full_name", 
        "email_id", 
        "phone_number", 
        "intrested_in_training"
    )
    
    search_fields = (
        "id", 
        "full_name", 
        "email_id", 
        "phone_number", 
        "intrested_in_training"
    )
    
@admin.register(NotificationTemplate)
class NotificationTemplatetModelAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "name", 
        "subject", 
        "content",
        "create_date",
        "modified_date",
    )
    
    list_filter = (
        "id", 
        "name", 
        "subject", 
        "content",
        "create_date",
        "modified_date",
    )
    
    search_fields = (
        "id", 
        "name", 
        "subject", 
        "content",
        "create_date",
        "modified_date",
    )