import sys
import threading
from timeit import default_timer as timer

from kivy.clock import Clock
from kivy.uix.popup import Popup

from cloudPrint.cloud_print import CLOUD_PRINT

from urls.connectionStatus.urls import web_working

from settings.configuration import EXITPASSWORD


class QR(Popup):

    def __init__(self, obj, **kwargs):
        super(QR, self).__init__(**kwargs)
        # TODO шалгах
        CLOUD_PRINT.set_time_values()

        self.obj = obj
        Clock.schedule_once(self.dismiss_popup, 60)
        Clock.schedule_interval(self.update, 0.6)

    def dismiss_popup(self, *args):
        CLOUD_PRINT.clear_file_response()
        Clock.unschedule(self.check_response)
        Clock.unschedule(self.check_file)
        Clock.unschedule(self.update)
        Clock.unschedule(self.dismiss_popup)
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.obj.sw_timer, 90)
        self.dismiss()

    def update(self, *args):
        global ExitPassword
        self.ids.qrInput.focus = True
        if self.ids.qrInput.text != '':
            if self.ids.qrInput.text == EXITPASSWORD:
                sys.exit()
            else:
                text = str(self.ids.qrInput.text)
                filecode = CLOUD_PRINT.check_qr_response(text)
                if filecode != None:
                    Clock.unschedule(self.update)
                    self.download_threading()
                    t5 = threading.Thread(target=CLOUD_PRINT.send_file_request(str(filecode)))
                    t5.start()
                else:
                    self.ids.QRText.text = "Та QR кодоо 2 удаа уншуулаад утсаа холдуулна уу."

            self.ids.qrInput.text = ""

    def download_threading(self):
        Clock.schedule_interval(self.check_response, 1)
        self.ids.QRText.color = 1, 1, 1, 1
        self.ids.QRText.text = "Уншиж байна. ТҮР ХҮЛЭЭНЭ ҮҮ."

    def check_response(self, *args):
        if web_working():
            if CLOUD_PRINT.get_file_status() is True:
                Clock.unschedule(self.dismiss_popup)
                self.ids.QRText.text = "ТАНЫ ФАЙЛЫГ ТАТАЖ БАЙНА. ТҮР ХҮЛЭЭНЭ ҮҮ."
                self.ids.QRText.color = 1, 1, 1, 1
                self.ids.qrPic.source = 'CLOUD_PRINT/asset/main/downloading.png'
                self.obj.clr_btn()
                self.obj.ids.Error_comment.text = ''
                Clock.unschedule(self.update)
                Clock.unschedule(self.check_response)
                Clock.schedule_interval(self.check_file, 1)
                t4 = threading.Thread(target=DownloadFile.process(CLOUD_PRINT.get_file_response(), UsrPathOb, UsrFileType))
                t4.start()
                t0 = threading.Thread(target=FileFixing)
                t0.start()
            else:
                Clock.schedule_interval(self.update, 0.5)
                self.ids.QRText.text = "ТАНЫ QR КОД АЛДААТАЙ БАЙНА."
                self.ids.QRText.color = 1, 0.1, 0.1, 1
                self.ids.qrInput.text = ''
                self.ids.qrInput.focus = True
                UsrFileRequest.ClearResponse()
        else:
            self.ids.QRText.text = "ХОЛБОЛТ САЛСАН БАЙНА."
            self.ids.QRText.color = 1, 1, 1, 1
            self.ids.qrPic.source = 'asset/main/Error.png'
            Clock.schedule_interval(self.update, 0.5)

    def check_file(self, *args):
        if DownloadFile.GetStatus() is True:
            self.dismiss()
            DownloadFile.ClearStatus()
            Clock.unschedule(self.check_response)
            self.File_Downloaded()

    def File_Downloaded(self, *args):
        self.dismiss()
        self.obj.QrCheck()
        UsrFileRequest.ClearResponse()
        Clock.unschedule(self.check_response)
        Clock.unschedule(self.check_file)
        Clock.unschedule(self.update)
        Clock.unschedule(self.dismiss_popup)
