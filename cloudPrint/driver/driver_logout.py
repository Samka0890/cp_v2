class DriverLogout:
    """
        Флаш орж ирсэн үгүйг мэдэх хэсэг
    """

    logout = True

    def get_driver_log_out(self):
        """
            DriverLogout object-ээс флаш байгааг эсэхийг авах функц
        """

        return self.logout

    def set_driver_log_out(self, logout):
        """
            DriverLogout object-ийн флаш байгааг эсэхийг утгыг солих функц
        """

        self.logout = logout
