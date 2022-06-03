import urllib
import requests
# from aiohttp import ClientSession
from urllib.request import urlopen
from settings.configuration import KIOSK


from utils.email.mail import send_mail_error


def web_working():
    try:
        url = 'https://www.cloudprint.mn'
        rsp = requests.get(url)

        web_status = False
        if rsp.status_code == 200:
            web_status = True

        # Өмнөх код
        # urlopen('https://www.cloudprint.mn', timeout=1)

        return web_status

    except Exception:
        return False

    # except urllib.error.URLError as Error:

    #     return False


def get_token():
    try:

        url = 'https://cloudprint.mn/api/auth/printer-auth'
        # TODO printer_id болон secret-ийг settings ээс авах
        body = {
            "printerId": "5f7c1738531578066647bbdb",
            "secret": "d#mq^7i6HXhVzNLU",
        }

        rsp = requests.post(url, body)

        if rsp.status_code != 200:
            return False

        data = rsp.json()

        return data['token']


        # Өмнөх код
        # Authentication_url = 'https://cloudprint.mn/api/auth/printer-auth'
        # Authentication_json = {
        #     'printerId': SetVariables.get_id(),
        #     'secret': SetVariables.get_secret()
        # }
        # # TODO шалгах
        # async with ClientSession() as session:
        #     async with session.post(Authentication_url, json=Authentication_json) as response:
        #         if response.status == 200:
        #             resp = await response.json()
        #             return resp['token']

    except Exception as err:
        send_mail_error(err, KIOSK['id'], KIOSK['location'])

        return ''
