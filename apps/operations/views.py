from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.authtoken.models import Token
from django.db import transaction
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import razorpay
import uuid
from decouple import config

# project import
from apps.operations.models.user import User, UserTypeChoice
from utils.bbb import create_meeting, join_meeting
from utils.permissions import IsAuthenticatedStudent, IsAuthenticatedTeacher
from utils.whatsapp_gateway import whatsapp_send_message
from apps.operations.models import TrainingForm, NotificationTemplate
from apps.operations.serializers import TrainingFormSerializers


def activation_token():
    return str(abs(hash(f"{uuid.uuid4()}")) % (10 ** 4))

class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'bad request'
    default_code = 'error'


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
            raise BadRequest("You are already part of Karostartup Family")
        client = razorpay.Client(auth=(config("RAZORPAY_A"), config("RAZORPAY_B")))
        link = client.payment_link.create({
                    "amount": 99900,
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


class UserViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        permissions = {
            "create_meeting": [IsAuthenticatedTeacher],
            "join_meeting": [IsAuthenticatedStudent],
            "request_register_otp": [AllowAny],
            "request_login_otp": [AllowAny],
            "verify_otp": [AllowAny],
        }
        permission_classes = permissions[self.action]
        return [permission() for permission in permission_classes]

    @action(methods=["POST"], detail=False, url_path="otp/register/request")
    def request_register_otp(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        name = request.data.get("name")
        user_type = request.data.get("type")
        if not (user_type and phone and name):
            raise BadRequest("type/name/phone not given")
        with transaction.atomic():
            user_entity = User.objects.filter(phone=phone).exists()
            if user_entity:
                raise BadRequest({"message": "User already registered"})
            user_entity = User.objects.create_user(
                phone=phone, name=name, user_type=user_type
            )
            whatsapp_template = NotificationTemplate.objects.get(name="register_whatsapp")
            whatsapp_send_message(
                body=whatsapp_template.content.format(
                    name=name, otp=user_entity.otp), to=phone)
            return Response(data={"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="otp/login/request")
    def request_login_otp(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        if not phone:
            raise BadRequest("phone not received")
        with transaction.atomic():
            user_entity = User.objects.filter(phone=phone).first()
            if not user_entity:
                return BadRequest({"message": "user not registered"})
            whatsapp_template = NotificationTemplate.objects.get(name="login_whatsapp")
            whatsapp_send_message(
                body=whatsapp_template.content.format(
                    name=user_entity.name, otp=user_entity.otp),
                to=user_entity.phone
            )
            return Response(data={"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="otp/verify")
    def verify_otp(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        token = request.data.get("token")
        with transaction.atomic():
            user_entity = User.objects.filter(phone=phone, otp=token).first()
            if not user_entity:
                raise BadRequest({"message": "token invalid"})
            token, created = Token.objects.get_or_create(user=user_entity)
            user_entity.otp = activation_token()
            user_entity.save()
            return Response({
                "user_type": user_entity.user_type,
                "token": token.key
            }, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="classroom/create")
    def create_meeting(self, request, *args, **kwargs):
        with transaction.atomic():
            create_classroom, meeting_id = create_meeting(request.user.name)
            for user in User.objects.filter(user_type=UserTypeChoice.STUDENT):
                link = join_meeting(user_name=user.name, meeting_id=meeting_id)
                user.classroom_link = link
                user.save()
            return Response(data={"message": "classroom created"}, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, url_path="classroom/join")
    def get_meeting_link(self, request, *args, **kwargs):
        user_entity = User.objects.get(id=request.user.id)
        return Response(data={"url": user_entity.classroom_link}, status=status.HTTP_200_OK)
