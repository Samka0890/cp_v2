"""
    Social Pay-тай холбоотой кодуудыг уг файлд бичнэ!
"""
import json
import requests

from urls.connectionStatus.urls import get_token
from utils.api.urls import SOCIALPAY_QR_RESPONSE
from utils.api.urls import CHECK_SOCIALPAY_PAYMENT


def socialpay_request(data):
    """
        Social Pay invoice үүсгэх функц
    """

    token = get_token()

    headers = {
        "X-Auth-Token": token,
    }

    rsp = requests.post(SOCIALPAY_QR_RESPONSE, json=data, headers=headers)

    if rsp.status_code != 200:
        # TODO Web дээр алдаа гарсан байна!
        return False, 'Веб дээр алдаа гарсан байна!'

    return True, rsp.json()


def socialpay_check_payment(data):
    """
        Social Pay хүсэлтийн төлбөр төлөгдсөн эсэхийг шалгах функц
    """

    token = get_token()

    headers = {
        "X-Auth-Token": token,
    }

    rsp = requests.post(CHECK_SOCIALPAY_PAYMENT, json=data, headers=headers)

    if rsp.status_code != 200:
        # TODO Web дээр алдаа гарсан байна!
        return False, 'Веб дээр алдаа гарсан байна!'

    return True, rsp.json()
