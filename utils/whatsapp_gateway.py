# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from decouple import config


account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
from_ = config("WHATSAPP")
client = Client(account_sid, auth_token)


def whatsapp_send_message(body: str, to: str, from_: str = from_,):
    try:
        message = client.messages.create(body=body, from_=f'whatsapp:{from_}', to=f'whatsapp:+91{to}')
        return message.sid
    except TwilioRestException:
        return "Not sent"
