from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from cloudPrint.cloud_print import CLOUD_PRINT
from utils.sound import sounds


Builder.load_file('pages/kv/main/main.kv')

class MainScreen(Screen):

    def __init__(self, **var_args):
        super(MainScreen, self).__init__(**var_args)
        self.BASE_DIR = ''
        self.check_pos = False
        self.pX = 10

    def on_enter(self, *args):
        CLOUD_PRINT.set_previous_page("main_screen")

    def sound_main(self):
        sounds.click_sound()

    def cancel_clock(self):
        Clock.unschedule(self.change_pos)
        self.ids.introduction.pos = self.width, self.height * 0.2

    def change_pos(self, *args):
        # NOTE True байвал гарч ирсэн байна
        if self.check_pos is True:
            if self.ids.introduction.x > self.width:
                Clock.unschedule(self.change_pos)
                Clock.unschedule(self.help_btn)
                self.check_pos = False
            else:
                self.ids.introduction.x += self.pX
        else:
            if self.ids.introduction.x < (self.width - self.width * 0.12):
                Clock.unschedule(self.change_pos)
                Clock.schedule_interval(self.help_btn, 10)
                self.check_pos = True
            else:
                self.ids.introduction.x -= self.pX

    def help_btn(self, *args):
        Clock.schedule_interval(self.change_pos, 0.02)
