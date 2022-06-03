import win32print

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.clock import Clock

from utils.sound.sounds import success_sound

from pages.screens.popup.feedBack.popup import FeedBackPopup

Builder.load_file('pages/kv/popup/printing/main.kv')

class PrintingPopup(Popup):

    def __init__(self, **kwargs):
        super(PrintingPopup, self).__init__(**kwargs)

    def timer(self):
        Clock.schedule_interval(self.check_printing, 1)

    def check_printing(self, *args):
        current_printer = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(current_printer)
        raw = win32print.EnumJobs(hPrinter, 0, 999)

        if len(raw) == 0:
            Clock.unschedule(self.check_printing)
            self.dismiss()
            pops = FeedBackPopup()
            pops.open()
            success_sound()

        win32print.ClosePrinter(hPrinter)
