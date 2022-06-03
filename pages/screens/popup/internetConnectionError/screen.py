from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup

from urls.connectionStatus.urls import web_working

Builder.load_file('pages/kv/popup/internetConnectionError/main.kv')


class InternetConnectionError(Popup):

    def __init__(self, **kwargs):
        super(InternetConnectionError, self).__init__(**kwargs)
        Clock.schedule_interval(self.check_status, 1)

    def popup_close(self, *args):
        Clock.unschedule(self.check_status)
        self.dismiss()

    def check_status(self, *args):
        if web_working():
            self.popup_close()

    pass
