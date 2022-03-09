from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

# project import
from utils.whatsapp_gateway import whatsapp_send_message
from apps.operations.models import TrainingForm, NotificationTemplate
from apps.operations.serializers import TrainingFormSerializers


# Create your views here.


class TrainingFormViewSet(viewsets.ModelViewSet):
    queryset = TrainingForm.objects.all()
    serializer_class = TrainingFormSerializers

    def create(self, request, *args, **kwargs):
        email = request.data.get("email_id")
        phone = request.data.get("phone_number")
        first_name = request.data.get("full_name").split()[0]
        is_data_present = TrainingForm.objects.filter(
            Q(email_id=email) | Q(phone_number=phone)
        ).exists()
        if not is_data_present:
            print("::::::::::>>>>>>>")
            serializer = TrainingFormSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = TrainingFormSerializers(request.data)
        email_template = NotificationTemplate.objects.get(name="internship_mail")
        send_mail(
            email_template.subject,
            email_template.content.format(first_name=first_name),
            settings.EMAIL_HOST_USER,
            [request.data.get("email_id")],
            fail_silently=True,
        )
        whatsapp_template = NotificationTemplate.objects.get(name="internship_whatsapp")
        whatsapp_send_message(body=whatsapp_template.content.format(first_name=first_name), to=phone)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

