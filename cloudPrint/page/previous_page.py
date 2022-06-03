class PreviousPage:
    """
        Хуудас аль хуудаснаас шилжиж ирснийг тохируулах хэсэг
    """
    previous_page = 'main_screen'
    on_print_page = False

    def get_previous_page(self):
        """
            PreviousPage object-ээс өмнөх хуудсыг авах функц
        """

        return self.previous_page

    def set_previous_page(self, page):
        """
            PreviousPage object-ийн өмнөх хуудсыг засах функц
        """

        self.previous_page = page

    def get_on_print_page(self):
        """
            PreviousPage object-ээс print page хуудас дээр хэрэглэгч байгааг эсэхийг авах функц
        """

        return self.on_print_page

    def set_on_print_page(self, state):
        """
            PreviousPage object-ийн print page хуудсыг утгыг засах функц
        """

        self.on_print_page = state
