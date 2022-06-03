from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup
from timeit import default_timer as timer

from settings.configuration import KIOSK
from cloudPrint.cloud_print import CLOUD_PRINT
from urls.additionals.additional import send_satisfaction

Builder.load_file('pages/kv/popup/star/main.kv')


class FeedBackPopup(Popup):

    def __init__(self, **kwargs):
        super(FeedBackPopup, self).__init__(**kwargs)
        Clock.schedule_once(self.popup_close, 10)
        self.rate = 5

    def popup_close(self, *args):

        send_satisfaction(KIOSK['id'], self.rate)
        CLOUD_PRINT.set_timer_duration(timer())
        # TODO log бичдэг болгох
        # LogWrite.success_log()
        self.dismiss()

    def feedback_rate(self, rate):
        self.rate = rate

    pass
