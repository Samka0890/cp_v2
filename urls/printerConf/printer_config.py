import requests

from utils.api.urls import PAPER_REDUCER_URL
from settings.configuration import KIOSK

from urls.connectionStatus.urls import get_token


def reduce_paper(reduced_page):
    """ Цаасны тоог өөрчлөх функц """

    token = get_token()

    headers = {
        "X-Auth-Token": token,
    }

    data = {"printerId": KIOSK['id'], "paperCount": int(reduced_page)}

    rsp = requests.post(PAPER_REDUCER_URL, json=data, headers=headers)

    if rsp.status_code == 200:
        return True, rsp.json()

    return False, 'Цаасны тоог вебээс авахад алдаа гарлаа!'
