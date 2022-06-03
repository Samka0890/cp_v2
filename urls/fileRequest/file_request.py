import requests

from settings.configuration import KIOSK

from urls.connectionStatus.urls import web_working

from utils.email.mail import send_mail_error

from pages.screens.popup.internetConnectionError.screen import InternetConnectionError


class FileRequest:

    # def __init__(self, response='', status=False):
    response = ''
    status = False

    def send_file_request(self, file_id):
        """
            Файл web дээр байгааг шалгах функц
        """

        if web_working():
            try:
                # NOTE файлын хэмжээнээс хамаарч байна уу? шалгах
                self.response = requests.get('https://cloudprint.mn/api/files/id/' + file_id, stream=True, timeout=20)
                if self.response.status_code == 200:
                    self.status = True
                else:
                    self.status = False

            except (requests.ConnectionError) as err:
                send_mail_error(err, KIOSK.get('id'), KIOSK.get('location'))
                self.status = False

                return False
        else:
            internet_connection_error_poppup = InternetConnectionError()
            internet_connection_error_poppup.open()


    def get_file_response(self):

        return self.response

    def get_file_status(self):

        return self.status

    def clear_file_response(self):
        self.response = ''
        self.status = False

        return True
