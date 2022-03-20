import json

import xmltodict
from decouple import config
import hashlib
from urllib.parse import urlencode
import requests
import uuid

bbbURL = config("BBB_URL")
bbbSecret = config("BBB_SECRET")


def create_meeting(user_name):
    meeting_id = uuid.uuid4().hex
    bbb_params = {
        'name': 'Karostartup Meeting',
        'meetingID': meeting_id,
        'attendeePW': 'ap',
        'moderatorPW': user_name,
        'record': 'true',
    }
    create_meeting_string = urlencode(bbb_params)
    checksum = hashlib.sha1(('create' + create_meeting_string + bbbSecret).encode('utf-8')).hexdigest()
    create_meeting_url = '{host}/create?{params}&checksum={checksum}'.format(
        host=bbbURL, params=create_meeting_string, checksum=checksum)
    response = requests.get(create_meeting_url)
    data = xmltodict.parse(response.text)
    return json.dumps(data), meeting_id


def join_meeting(user_name, meeting_id):
    join_params = {
        'fullName': user_name,
        'meetingID': meeting_id,
        'password': "mp"
    }
    create_meeting_string = urlencode(join_params)
    checksum = hashlib.sha1(('join' + create_meeting_string + bbbSecret).encode('utf-8')).hexdigest()
    join_meeting_url = '{host}/join?{params}&checksum={checksum}'.format(
        host=bbbURL, params=create_meeting_string, checksum=checksum)
    return join_meeting_url
