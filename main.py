import os

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform as core_platform

from pages.screens.main.screen import MainScreen
from pages.screens.offline.screen import OfflineScreen
from pages.screens.printOpt.screen import PrintScreen
from pages.screens.online.screen import OnlineScreen

# NOTE CloudPrint object-ийг байгуулж байна!
from cloudPrint.cloud_print import CloudPrint

from pages.screens.main.timeLabel.time_label import TimeLabel


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

TITLE = 'CloudPrint'

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('postproc', 'retain_time', '50')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'window_state', 'maximized')
Config.write()

filesize_units = ('B', 'KB', 'MB', 'GB', 'TB')
Window.clearcolor = (0.95, 0.95, 0.95, 1)
checkerVariable = ['.DS_Store']
platform = core_platform
_have_win32file = False
# Window.borderless = True
# Window.fullscreen = 'auto'


class ScreenManagement(ScreenManager):
    pass


class LabelBtn(ButtonBehavior, Label):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


screen_manager = Builder.load_file(os.path.join(BASE_DIR, 'pages/kv/screenManager.kv'))


class MainApp(App, TimeLabel):

    def on_start(self, *args):
        # Clock.schedule_once(self.Golomt, 1)
        Window.set_title(TITLE)
        Window.bind(on_request_close=self.on_request_close)
        # # Register top-most
        # # register_topmost(Window, TITLE)
        # if CheckStatus():
        #     resp = post_reduce_paper(0)
        #     LeftPaper.set_left_paper(resp['paper'])
        # else:
        #     InternetConnectionErrorPopup()

    def build(self):
        # NOTE main.kv file-ийн path
        self.icon = 'pages/kv/assets/images/CP_logo.png'

        # with open("/home/sukhee/cloudPrint/pages/main.kv", encoding='utf8') as f:
        #     presentation = Builder.load_string(f.read())
        #     f.close()
        # TimeLabel()
        # reset_folder('CloudPrint/Flash_Check')
        # os.system("C:/CP/POSInitialize/InitializeKey.exe")
        return screen_manager

    def on_request_close(self, *args):
        return True


if __name__ == '__main__':
    MainApp().run()


# import win32api
# import win32print

# p_name = win32print.GetDefaultPrinter()
# # filename = "C:/Users/svhba/OneDrive/Desktop/sukhee_test_v1.pdf"
# filename = "C:/Users/svhba/OneDrive/Desktop/sukhee_test.pdf"

# GHOSTSCRIPT_PATH = "C:/Users/svhba/OneDrive/Desktop/cloudPrint/cloudPrint/GHOSTSCRIPT/bin/gswin32.exe"
# GSPRINT_PATH = "C:/Users/svhba/OneDrive/Desktop/cloudPrint/cloudPrint/GSPRINT/gsprint.exe"

# # YOU CAN PUT HERE THE NAME OF YOUR SPECIFIC PRINTER INSTEAD OF DEFAULT
# current_printer = win32print.GetDefaultPrinter()
# # '-ghostscript "'+ GHOSTSCRIPT_PATH + '" -printer "' + current_printer + '"' + ' "' + filename + '"'
# params = """-ghostscript "{GHOSTSCRIPT_PATH}" -printer "{current_printer}" "{filename}" """.format(
#     GHOSTSCRIPT_PATH=GHOSTSCRIPT_PATH,
#     current_printer=current_printer,
#     filename=filename
# )

# win32api.ShellExecute(
#     0,
#     'open',
#     GSPRINT_PATH,
#     # '-ghostscript "'+ GHOSTSCRIPT_PATH + '" -printer "' + current_printer + ' "' + filename + '"',
#     '-ghostscript "'+ GHOSTSCRIPT_PATH + '" -printer "' + current_printer + '"' + ' "' + filename + '"',
#     '.',
#     0
# )

# print('done')
