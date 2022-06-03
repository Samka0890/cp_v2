import requests

from utils.api.urls import FILE_CONFIG_URL


def get_file_config(filename):
    """
        Web-аас файлын хэвлэх тохиргоог авах функц
    """

    url = FILE_CONFIG_URL + filename

    rsp = requests.Response()
    rsp.status_code = 404

    try:
        rsp = requests.get(url, timeout=30)

    except Exception:
        pass

    return rsp
