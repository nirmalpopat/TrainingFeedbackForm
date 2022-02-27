from django.contrib import admin

# project imports
from apps.operations.models import TrainingInformations
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