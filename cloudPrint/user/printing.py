class Printing:
    """
        Хэрэглэгчийн файлыг хэвлэх хэсэг
    """

    color_value = '-color'
    copies_number = 1
    page_chooser_value = True
    page_input_value = ''
    return_offline_page = False
    paper_duplex = ''
    page_orientation = '-portrait'
    req_duplex = False
    total_cash = 0
    color_type = 'colored'   # web-ээс авахдаа
    printed_page = 0
    pages_input_check_state = False

    def color_value_change(self, color_value):
        self.color_value = color_value

    def copies_number_change(self, copies_number):
        check_copies_number = self.copies_number + int(copies_number)
        if check_copies_number > 0 and check_copies_number < 101:
            self.copies_number = check_copies_number

    def page_chooser_value_change(self, page_chooser_value):
        self.page_chooser_value = page_chooser_value

    def page_input_value_change(self, page_input_value):
        self.page_input_value = page_input_value

    def paper_duplex_change(self, paper_duplex):
        self.paper_duplex = paper_duplex

    def page_orientation_change(self, page_orientation):
        self.page_orientation = page_orientation

    def req_duplex_change(self, req_duplex):
        self.req_duplex = req_duplex

    def color_type_change(self, color_type):
        self.color_type = color_type

    def printed_page_change(self, total_page):
        self.printed_page = total_page

    def total_cash_change(self, total_cash):
        self.total_cash = total_cash

    def pages_input_check_state_change(self, state):
        self.pages_input_check_state = state

    # --------------------- get functions ---------------------
    def get_color_value(self):
        return self.color_value

    def get_copies_number(self):
        return self.copies_number

    def get_page_chooser_value(self):
        return self.page_chooser_value

    def get_page_input_value(self):
        return self.page_input_value

    def get_paper_duplex(self):
        return self.paper_duplex

    def get_page_orientation(self):
        return self.page_orientation

    def get_req_duplex(self):
        return self.req_duplex

    def get_color_type(self):
        return self.color_type

    def get_printed_page(self):
        return self.printed_page

    def get_total_cash(self):
        return self.total_cash

    def get_pages_input_check_state(self):
        return self.pages_input_check_state

    def reset(self):
        """
            Printer-ийн тохиргоо анхны төлөвд оруулах
        """

        self.color_value = '-color'
        self.copies_number = 1
        self.page_chooser_value = True
        self.page_input_value = ''
        self.return_offline_page = False
        self.paper_duplex=''
        self.page_orientation = '-portrait'
        self.req_duplex = False
        self.color_type = 'colored'
        self.printed_page=0
        self.total_cash=0
        self.pages_input_check_state = False
