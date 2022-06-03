from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup

from cloudPrint.cloud_print import CLOUD_PRINT

Builder.load_file('pages/kv/popup/loading/main.kv')


class Loading_Popup(Popup):

    def __init__(self, PrintScreen, **kwargs):
        super(Loading_Popup, self).__init__(**kwargs)
        self.PrintScreen = PrintScreen
        Clock.schedule_interval(self.chech_signal, 0.5)

    def chech_signal(self, *args):
        Clock.unschedule(self.chech_signal)
        self.PrintScreen._print_service()
        self.dismiss()

    def CancelBtn(self, *args):
        Clock.unschedule(self.chech_signal)


class Loading_Continue_Popup(Popup):

    def __init__(self, PrintScreen, **kwargs):
        super(Loading_Continue_Popup, self).__init__(**kwargs)
        self.PrintScreen = PrintScreen
        Clock.schedule_interval(self.check_signal, 0.5)

    def check_signal(self, *args):
        if CLOUD_PRINT.get_timer_duration() != 0:
            Clock.unschedule(self.check_signal)
            self.dismiss()
            if (CLOUD_PRINT.get_printed_page() > CLOUD_PRINT.get_printer_paper() - 10):
                self.PrintScreen.Caution_PP()
            else:
                self.PrintScreen.payment_pp()

    def cancel_btn(self, *args):
        Clock.unschedule(self.check_signal)
