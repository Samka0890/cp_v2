# Хэрэглэгчийн уншуулсан QR кодыг задлах, хадгалах хэсэг
import json

# from cloudPrint.cloud_print import CLOUD_PRINT

from urls.fileRequest.file_config import get_file_config


class QrReader:
    # NOTE хуучин код
    # def __init__(self, filename = '', direct_print = False):
    #     from constants.constants import CLOUD_PRINT

    #     self.filename = filename
    #     self.direct_print = direct_print

    #     CLOUD_PRINT.reset()

    filename = ''
    direct_print = False

    def check_qr_response(self, qr_response):
        print("qr_response >>>", qr_response)

        response = self.validate_json(qr_response)
        if response is not False:
            if response["setConfig"] == 'true':

                config_response = get_file_config(response["filename"])
                if config_response is not False:
                    CLOUD_PRINT.copies_number_change(int(config_response[0]["copies"]))

                    color_value = '-gray'
                    if config_response[0]["colortype"] == 'true':
                        color_value = '-color'

                    CLOUD_PRINT.color_value_change(color_value)

                    paper_duplex = ''
                    if config_response[0]["side"] == 'true':
                        paper_duplex = '-duplex'

                    CLOUD_PRINT.paper_duplex_change(paper_duplex)

                    if config_response[0]["pages"] != 'all':
                        CLOUD_PRINT.page_input_value_change(config_response[0]["pages"])

                    CLOUD_PRINT.page_chooser_value_change(False)

                    page_orientation = '-landscape'
                    if response["layout"] == 'true':
                        page_orientation = '-portrait'

                    CLOUD_PRINT.page_orientation_change(page_orientation)

                    self.direct_print = True

                    return response["filename"]
                else:
                    self.direct_print = False

                    return response["filename"]

            else:
                self.direct_print = False

                return response["filename"]

        else:
            print("Таны уншуулсан QR код буруу байна.")

    def validate_json(self, response):
        try:
            json_string = json.loads(response)
            if type(json_string) is not int:
                return json_string
            else:
                return False

        except ValueError as err:
            return False

    def get_direct_print(self):
        return self.direct_print

    def direct_print_reset(self):
        self.direct_print = False



# {"filename":"x5OkyHKj3j","setConfig":"false"}
