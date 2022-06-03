from datetime import datetime

from kivy.clock import Clock
from kivy.uix.label import Label


class TimeLabel(Label):

    def __init__(self, **kwargs):
        super(TimeLabel, self).__init__(**kwargs)
        now = datetime.now()
        self.text = str(now.strftime("%H:%M"))
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        now = datetime.now()
        self.text = str(now.strftime("%H:%M"))
