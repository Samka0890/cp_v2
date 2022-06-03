class Printer:
    paper = 500

    def get_printer_paper(self):
        """
            printer-ийн цаасны хэмжээг авах функц
        """

        return self.paper

    # setter method
    def set_printer_paper(self, paper):
        """
            printer-ийн цаасны хэмжээг солих функц
        """

        self.paper = paper

    def reset_printer_paper(self):
        """
            printer-ийн цаасны хэмжээг солих функц
        """

        self.paper = 500
