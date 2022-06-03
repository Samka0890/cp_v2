from kivy.lang import Builder
from kivy.uix.popup import Popup

Builder.load_file('pages/kv/popup/payment/main.kv')


class Payment_Popup(Popup):
    def __init__(self, obj, **kwargs):
        super(Payment_Popup, self).__init__(**kwargs)
        self.obj = obj
