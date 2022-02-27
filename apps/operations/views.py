from django.shortcuts import render
from rest_framework import viewsets

# project import
from apps.operations.models import TrainingInformations
from apps.operations.serializers import TrainingInformationsSerializers

# Create your views here.
class TrainingInformationsViewSet(viewsets.ModelViewSet):
    queryset = TrainingInformations.objects.all()
    serializer_class = TrainingInformationsSerializers