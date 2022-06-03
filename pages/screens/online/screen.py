import os
import threading

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from utils.sound import sounds
from utils.fileDownload.file_download import download_file
from utils.file.file import pdf_to_image

from cloudPrint.cloud_print import CLOUD_PRINT

from urls.connectionStatus.urls import web_working

from pages.screens.popup.qr.popup import QR


Builder.load_file('pages/kv/online/main.kv')


class OnlineScreen(Screen):

    def __init__(self, **kwargs):
        super(OnlineScreen, self).__init__(**kwargs)
        self.letter_up = False

    def sw_timer(self, *args):
        if self.parent is not None:
            self.parent.transition.direction = 'left'
            self.parent.current = "main_screen"
            Clock.unschedule(self.sw_timer)

    def on_enter(self, *args):
        CLOUD_PRINT.set_previous_page('Online')
        Clock.schedule_interval(self.sw_timer, 90)

    def on_leave(self, *args):
        self.letter_up = True
        self.btn_one_clk()

    def time_out(self, *args):
        self.parent.transition.direction = 'left'
        self.parent.current = 'main_screen'
        self.ids.Error_comment.text = ""
        self.ids.Back_page.disabled = False
        self.clr_btn()

    def register(self):
        # -------------------------------SEND REQUEST TO SERVER----------------------------------
        sounds.click_sound()

        # NOTE test
        file_name = 'ypuEjLEYFd'
        CLOUD_PRINT.send_file_request(file_name)

        if CLOUD_PRINT.get_file_status():
            self.ids.Error_comment.text = "Уншиж байна. ТҮР ХҮЛЭЭНЭ ҮҮ."
            is_downloaded = download_file(CLOUD_PRINT.get_file_response())

            if is_downloaded:
                CLOUD_PRINT.set_on_print_page(True)
                # TODO шалгах!
                # t0 = threading.Thread(target=FileFixing)
                # t0.start()
                self.ids.Back_page.disabled = False
                self.setConfigure()
                self.ids.Error_comment.text = ""
                self.parent.current = "print_screen"
                self.clr_btn()
            else:
                raise Exception('file татахад алдаа гарлаа!')

        if len(self.ids.input.text) == 10:
            if web_working():
                self.ids.Back_page.disabled = True
                CLOUD_PRINT.send_file_request(self.ids.input.text)
                # NOTE файл web дээр байна гэсэн үг
                if CLOUD_PRINT.get_file_status():
                    self.ids.Error_comment.text = "Уншиж байна. ТҮР ХҮЛЭЭНЭ ҮҮ."
                    is_downloaded = download_file(CLOUD_PRINT.get_file_response())

                    # TODO файл татахад алдаа гарсан учир дахин эхлүүлэх
                    # Эсвэл интернэтээс болж байвал өөр арга хэмжээ авах
                    if not is_downloaded:
                        raise Exception('file татахад алдаа гарлаа!')

                    CLOUD_PRINT.set_on_print_page(True)
                    # TODO шалгах!
                    # t0 = threading.Thread(target=FileFixing)
                    # t0.start()
                    self.ids.Back_page.disabled = False
                    self.setConfigure()
                    self.ids.Error_comment.text = ""
                    self.parent.current = "print_screen"
                    self.clr_btn()
                else:
                    self.ids.Back_page.disabled = False
                    self.ids.Error_comment.text = "Алдаатай байна. Та оруулсан дугаараа шалгана уу!"
            else:
                self.ids.Error_comment.text = "ХОЛБОЛТ САЛСАН БАЙНА."
        else:
            self.ids.Error_comment.text = "Файлын дугаараа зөв оруулна уу!"

    def chkUserNum(self):
        # -------------------------------USER CODE INPUT----------------------------------
        sounds.click_sound()
        if len(self.ids.input.text) > 10:
            self.ids.input.text = self.ids.input.text[:-1]
        if len(self.ids.input.text) == 10:
            self.ids.Error_comment.text = "Та үргэлжлүүлэх үү?"

    def clr_btn(self):
        sounds.click_sound()
        self.ids.input.text = ''
        Clock.unschedule(self.sw_timer)

    def btn_one_clk(self):
        self.letter_up = not self.letter_up
        if self.letter_up is True:
            self.ids.bq.text = 'Q'
            self.ids.bw.text = 'W'
            self.ids.be.text = 'E'
            self.ids.br.text = 'R'
            self.ids.bt.text = 'T'
            self.ids.by.text = 'Y'
            self.ids.bu.text = 'U'
            self.ids.bi.text = 'I'
            self.ids.bo.text = 'O'
            self.ids.bp.text = 'P'
            self.ids.ba.text = 'A'
            self.ids.bs.text = 'S'
            self.ids.bd.text = 'D'
            self.ids.bf.text = 'F'
            self.ids.bg.text = 'G'
            self.ids.bh.text = 'H'
            self.ids.bj.text = 'J'
            self.ids.bk.text = 'K'
            self.ids.bl.text = 'L'
            self.ids.bz.text = 'Z'
            self.ids.bx.text = 'X'
            self.ids.bc.text = 'C'
            self.ids.bv.text = 'V'
            self.ids.bb.text = 'B'
            self.ids.bn.text = 'N'
            self.ids.bm.text = 'M'
        else:
            self.ids.bq.text = 'q'
            self.ids.bw.text = 'w'
            self.ids.be.text = 'e'
            self.ids.br.text = 'r'
            self.ids.bt.text = 't'
            self.ids.by.text = 'y'
            self.ids.bu.text = 'u'
            self.ids.bi.text = 'i'
            self.ids.bo.text = 'o'
            self.ids.bp.text = 'p'
            self.ids.ba.text = 'a'
            self.ids.bs.text = 's'
            self.ids.bd.text = 'd'
            self.ids.bf.text = 'f'
            self.ids.bg.text = 'g'
            self.ids.bh.text = 'h'
            self.ids.bj.text = 'j'
            self.ids.bk.text = 'k'
            self.ids.bl.text = 'l'
            self.ids.bz.text = 'z'
            self.ids.bx.text = 'x'
            self.ids.bc.text = 'c'
            self.ids.bv.text = 'v'
            self.ids.bb.text = 'b'
            self.ids.bn.text = 'n'
            self.ids.bm.text = 'm'

    def qs_sign(self):
        sounds.click_sound()
        Clock.unschedule(self.sw_timer)
        QPAY = QR(self)
        QPAY.open()
        Clock.schedule_interval(self.CheckPPClosed, 1)
        Clock.schedule_interval(self.QrCheck, 1)

    def CheckPPClosed(self, *args):
        Clock.unschedule(self.CheckPPClosed)
        Clock.unschedule(self.QrCheck)

    def QrCheck(self, *args):
        self.setConfigure()
        Clock.unschedule(self.QrCheck)

    def setConfigure(self):
        t1 = threading.Thread(target=slide_change(self))
        file_path = os.path.join(CLOUD_PRINT.get_base_dir(), CLOUD_PRINT.get_document_name())
        t2 = threading.Thread(target=pdf_to_image(file_path, 50))

        t1.start()
        t2.start()

def slide_change(self):
    self.parent.transition.direction = 'right'
    self.parent.current = 'print_screen'
    self.parent.ids.print_screen.rightButton.disabled = True
    self.parent.ids.print_screen.leftButton.disabled = True
    self.parent.ids.print_screen.slider.disabled = True
