from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup

from cloudPrint.cloud_print import CLOUD_PRINT

Builder.load_file('pages/kv/popup/printer_paper/main.kv')


class CheckLeftPaperPopup(Popup):

    def __init__(self, **kwargs):
        super(CheckLeftPaperPopup, self).__init__(**kwargs)
        Clock.schedule_once(self.popup_close, 10)
        self.ids.caution.text = "Төхөөрөмж " + str(CLOUD_PRINT.get_printer_paper() - 10) + " хуудас хэвлэх боломжтой байна."

    def popup_close(self, *args):
        self.dismiss()

    pass
