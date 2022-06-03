import datetime as dt

from settings.global_variables import USER_TIME


class UserTimer:
    """
        Хэрэглэгчийн киоск ашиглаж буй хугацааг хэмжиж буй класс
    """
    start_time = ''
    end_time = ''

    def get_user_timer(self):
        """
            Хэрэглэгчийн киоскийг ашиглаж эхэлсэн хугацааг болон дуусах хугацааг авах функц
            return start_time, end_time
        """

        return self.start_time, self.end_time

    def set_time_values(self):
        """
            Хэрэглэгчийн хугацааг шинэчлэх
        """

        now = dt.datetime.now().time()
        duration = dt.timedelta(minutes=USER_TIME)
        end = (dt.datetime.combine(dt.date(1, 1, 1), now) + duration).time()

        self.start_time = now
        self.end_time = end
