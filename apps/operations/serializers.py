# lib imports
from rest_framework import serializers

# project imports
from apps.operations.models import TrainingForm


class TrainingFormSerializers(serializers.ModelSerializer):
    class Meta:
        model = TrainingForm
        fields = "__all__"
        read_only_fields = ("id", "create_date", "modified_date")
        datetime_fields = ("create_date", "modified_date")
