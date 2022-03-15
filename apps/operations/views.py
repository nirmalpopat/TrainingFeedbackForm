from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import razorpay
from decouple import config

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
        interested_in_training = request.data.get("intrested_in_training")
        request.data["interested_in_training"] = interested_in_training
        is_data_present = TrainingForm.objects.filter(
            Q(email_id=email) | Q(phone_number=phone)
        ).exists()
        if not is_data_present:
            serializer = TrainingFormSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = TrainingFormSerializers(request.data)
        client = razorpay.Client(auth=(config("RAZORPAY_A"), config("RAZORPAY_B")))
        link = client.payment_link.create({
                    "amount": config("RAZORAY_AMOUNT"),
                    "currency": "INR",
                    "accept_partial": False,
                    "description": "Karostartup Payment",
                    "customer": {
                        "name": request.data.get("full_name"),
                        "email": email,
                        "contact": f"+91{phone}"
                         },
                    "notify": {
                        "sms": False,
                        "email": False
                        },
                    "reminder_enable": False,
                    "callback_method": "get"
                }
        )
        email_template = NotificationTemplate.objects.get(name="internship_mail")
        send_mail(
            email_template.subject,
            email_template.content.format(first_name=first_name, link=link.get("short_url")),
            settings.EMAIL_HOST_USER,
            [request.data.get("email_id")],
            html_message=email_template.content.format(first_name=first_name, link=link.get("short_url")),
            fail_silently=True,
        )
        whatsapp_template = NotificationTemplate.objects.get(name="internship_whatsapp")
        whatsapp_send_message(body=whatsapp_template.content.format(first_name=first_name, link=link.get("short_url")), to=phone)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

