import requests

from utils.api.urls import USER_SATISFACTION_URL
from urls.connectionStatus.urls import get_token


def send_satisfaction(id, point):

    token = get_token()

    headers = {
        "X-Auth-Token": token,
    }

    data = {"printerId": id, "point": point}

    response = requests.post(USER_SATISFACTION_URL, json=data, headers=headers)

    if response.status_code == 200:
        return True, response.json()

    return False, 'Хэрэглэгчийн сэтгэл ханамжийг илгээхэд алдаа гарлаа!'
