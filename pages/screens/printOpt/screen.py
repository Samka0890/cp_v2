import re

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from pages.screens.popup.payment.screen import Payment_Popup
from pages.screens.popup.socail_pay.screen import SocialPay_Popup

from pages.screens.popup.loading.screen import Loading_Popup
from pages.screens.popup.loading.screen import Loading_Continue_Popup
from pages.screens.popup.printing.popup import PrintingPopup

from cloudPrint.cloud_print import CLOUD_PRINT

from urls.connectionStatus.urls import get_token

from utils.sound import sounds
from utils.folder.folder import reset_folder

from utils.printer.printer import printing

from urls.printerConf.printer_config import reduce_paper


Builder.load_file('pages/kv/printOpt/main.kv')


class PrintScreen(Screen):

    kb_x = 0
    kb_y = 0
    allPage = 0
    color = CLOUD_PRINT.get_color_value()

    def __init__(self, **kwargs):
        super(PrintScreen, self).__init__(**kwargs)
        self.pic_reloaded = 0

    def on_enter(self, *args):
        Clock.schedule_interval(self.update, 0.5)
        self.cash_calculator()
        CLOUD_PRINT.set_on_print_page(True)
        # TODO байнга авах шаардлагатай юу шалгах
        get_token()
        if CLOUD_PRINT.direct_print is True:
            self.Loading_direct_print_PP()

    def on_leave(self, *args):
        CLOUD_PRINT.set_on_print_page(False)
        CLOUD_PRINT.direct_print_reset()
        Clock.unschedule(self.update)

    def update(self, *args):
        # TODO шалгах
        # if GhostWorking.get_office_status() is True:
        #     self._page_number()

        if CLOUD_PRINT.get_timer_duration() != 0:
            if self.pic_reloaded == 0:
                self.ids.imageView.source = 'cloudPrint/save_image/image0.png'
                self.ids.imageView.reload()
                self.cash_calculator()
                self.allPage = CLOUD_PRINT.get_total_page()
                self.ids.slider_all.text = "         /    " + str(self.allPage)
                self.pic_reloaded += 1
                self.ids.loading_text.opacity = 0
                self.ids.rightButton.disabled = False
                self.ids.leftButton.disabled = False
                self.ids.slider.disabled = False
                Clock.unschedule(self.update)

            if CLOUD_PRINT.get_direct_print() is True:
                self.color = CLOUD_PRINT.get_color_value()
                self.ids.copies_input.text = str(CLOUD_PRINT.get_copies_number())

                if CLOUD_PRINT.get_color_value() == "-color":
                    self.ids.lab_colorful.pos_hint = {'x': .475, 'y': .275}
                else:
                    self.ids.lab_colorful.pos_hint = {'x': .705, 'y': .275}

                if CLOUD_PRINT.get_page_input_value() == '':
                    CLOUD_PRINT.page_input_value_change('1-' + str(CLOUD_PRINT.get_total_page()))

                self.ids.lab_all.opacity = 0
                self.ids.lab_custom.opacity = 1
                self.ids.pageNum_input.opacity = 1
                self.ids.pageNum_input.text = CLOUD_PRINT.get_page_input_value()
                self.ids.pageNum_input.disabled = True
                self.ids.btn_custom.color = 0.95,0.95,0.95,1
                self.ids.btn_all.color = 0.1,0.1,0.1,1
                self.ids.all_caption.opacity = 0

    def reset_timer(self):
        CLOUD_PRINT.set_on_print_page(False)
        # if GhostWorking.get_status() is False:
        #     GhostWorking.kill_ghost()
        self.pic_reloaded = 0
        CLOUD_PRINT.reset_timer()
        # GhostWorking.clear_status()
        CLOUD_PRINT.clear_total_page()
        CLOUD_PRINT.reset()
        sounds.click_sound()

        folder_name = 'cloudPrint/save_image'
        reset_folder(folder_name)

    def print_sound(self):
        sounds.click_sound()

    def _print_service(self, *args):
        copies_number = CLOUD_PRINT.get_copies_number()
        color_value = CLOUD_PRINT.get_color_value()
        page_chooser_value = CLOUD_PRINT.get_page_chooser_value()
        paper_duplex = CLOUD_PRINT.get_paper_duplex()
        page_orientation = CLOUD_PRINT.get_page_orientation()

        # NOTE ghost ашиглахгүй байхаар хийж байна!
        # if GhostWorking.get_status() is True:
        Clock.unschedule(Loading_Popup.chech_signal)

        # NOTE энэ юу хийж байгаа вэ? шалгах
        CLOUD_PRINT.reset_timer()
        sounds.click_sound()

        # -------------------------------PAGE NUMBER PROTECTION----------------------------------
        if page_chooser_value is False:
            data_page_number = self.ids.pageNum_input.text
            if(data_page_number == ''):
                data_page_number = '1' + '-' + str(CLOUD_PRINT.get_total_page())
        else:
            data_page_number = '1' + '-' + str(CLOUD_PRINT.get_total_page())
        # -------------------------------READ PDF FILE PAGES NUM----------------------------------
        # -------------------------------PDF SAVE----------------------------------
        inputArray = data_page_number
        To_array = inputArray.split(",")
        page_counter = 0
        for i in To_array:
            if i.find("-") != -1:
                save_array = i.split("-")
                # --------------------------------- Хэрэглэгчийн файлыг хэвлэнэ ---------------------------------
                printing(int(save_array[0]), int(save_array[1]))
            else:
                # --------------------------------- Хэрэглэгчийн файлыг хэвлэнэ ---------------------------------
                printing(int(i), int(i))
        self._printing_popup()
        # TODO Шалгах
        # else:
        #     Clock.unschedule(Loading_Popup.chech_signal)
        #     self.Loading_Popup()

    def page_number(self):
        # ------------------------TEXT INPUT LIMIT---------------------------
        page_input_value = self.ids.pageNum_input.text
        if page_input_value != '':
            pattern = '0123456789,-'  # zuwshuurugduh temdegtuud
            str_count = 0
            for one_char in page_input_value:
                if pattern.find(one_char) != -1:
                    str_count += 1
            if (str_count == len(page_input_value)):
                if page_input_value.find(',,') != -1 or page_input_value.find('--') != -1 or page_input_value.find(',-') != -1 or page_input_value.find('-,') != -1:
                    self.ids.Error_comment.text = "Алдаатай байна. Дараах тэмдэгтүүд орсон байна. (,,)(--)(,-)(-,)"
                    self.ids.print_service.disabled = True
                    CLOUD_PRINT.pages_input_check_state_change(True)
                elif page_input_value.startswith(',') or page_input_value.endswith(',') or page_input_value.startswith('-') or page_input_value.endswith('-'):
                    self.ids.print_service.disabled = True
                    self.ids.Error_comment.text = "Алдаатай байна. Эхлэл эсвэл төгсгөл хэсгийн тэмдэгтүүд."
                    CLOUD_PRINT.pages_input_check_state_change(True)
                else:
                    max_page = re.findall('\\d+', page_input_value)
                    max_page = map(int, max_page)
                    max_page = max(max_page)
                    # TODO шалгах
                    # if GhostWorking.get_office_status() is True or str(UsrFileType.GetFileType()) == 'pdf':
                    if CLOUD_PRINT.get_file_type() == 'pdf':
                        if (max_page <= CLOUD_PRINT.get_total_page()):
                            self.ids.Error_comment.text = ''
                            self.ids.print_service.disabled = False
                            CLOUD_PRINT.pages_input_check_state_change(False)
                            CLOUD_PRINT.page_input_value_change(page_input_value)
                        else:
                            self.ids.print_service.disabled = True
                            self.ids.Error_comment.text = "Хуудсын нийт тоо " + str(CLOUD_PRINT.get_total_page()) + " байх ёстой."
                            CLOUD_PRINT.pages_input_check_state_change(True)
                    else:
                        self.ids.Error_comment.text = "Таны файлыг уншиж байна."

            else:
                self.ids.print_service.disabled = True
                self.ids.Error_comment.text = "Алдаатай хэмжээс. Дараах загварын дагуу оруулна уу!(1-5,8,11-13)"
                CLOUD_PRINT.pages_input_check_state_change(True)

    def set_slider(self, value):
        max_value = CLOUD_PRINT.get_total_page()
        self.ids.slider.max = max_value
        if self.ids.slider.value + value <= max_value and self.ids.slider.value + value > 0:
            self.ids.slider.value += value
            self.ids.slider_text.text = str(int(self.ids.slider.value)) + ' '
            # self.ids.imageView.source = ConvertedImages + str(int(self.ids.slider.value) - 1) + "_outputA6.pdf.jpg"
            self.ids.imageView.source = 'cloudPrint/save_image/image' + str(int(self.ids.slider.value) - 1) + '.png'
            self.ids.imageView.reload()

    def page_value(self, selected_value):
        CLOUD_PRINT.page_chooser_value_change(selected_value)
        if selected_value is True:
            self.ids.print_service.disabled = False
        else:
            self.ids.print_service.disabled = True

    def _copies_number(self, value):
        CLOUD_PRINT.copies_number_change(value)
        self.ids.copies_input.text = str(CLOUD_PRINT.get_copies_number())

    def color_choose(self, color_value):
        CLOUD_PRINT.color_value_change(color_value)
        self.color = color_value

    def _key_correct(self):
        if self.ids.pageNum_input.text == '':
            self.ids.pageNum_input.text = '1-' + str(CLOUD_PRINT.get_total_page())

    def return_page(self):
        if CLOUD_PRINT.get_previous_page() == 'online_screen':
            self.parent.transition.direction = 'left'
            self.parent.current = "online_screen"
            CLOUD_PRINT.set_previous_page('online_screen')
        else:
            self.parent.transition.direction = 'right'
            self.parent.current = "offline_screen"
            CLOUD_PRINT.set_previous_page('offline_screen')
            CLOUD_PRINT.set_document_name('')

    def check_duplex(self, paper_duplex_value):
        CLOUD_PRINT.paper_duplex_change(paper_duplex_value)

    def check_orientation(self, page_orientation):
        CLOUD_PRINT.page_orientation_change(page_orientation)

    def _printing_popup(self):

        # TODO цаас шалгаж байгааг төлбөр төлөхийн өмнө хийх!
        success, data = reduce_paper(CLOUD_PRINT.get_printed_page())

        if success:
            CLOUD_PRINT.set_printer_paper(data['paper'])

            self.parent.transition.direction = 'right'
            self.parent.current = "main_screen"
            self.page_value(True)
            self.ids.pageNum_input.text = ''
            self.ids.copies_input.text = '1'
            self.ids.slider.value = 1
            self.ids.lab_all.opacity = 1
            self.ids.lab_custom.opacity = 0
            self.ids.pageNum_input.opacity = 0
            self.ids.pageNum_input.disabled = True
            self.ids.btn_custom.color = 0, 0, 0, 1
            self.ids.btn_all.color = 0.95, 0.95, 0.95, 1
            self.ids.all_caption.opacity = 1
            self.ids.pageNum_input.text = ''
            self.ids.Error_comment.text = ''
            self.ids.lab_colorful.pos_hint = {'x': .475, 'y': .275}
            self.ids.lab_colorful.opacity = 1
            self.ids.lab_colorless.disabled = False
            self.ids.lab_colorless.opacity = 1
            self.ids.lab_colorless.pos_hint = {'x': 0.465, 'y': 0.3}
            self.ids.btn_colorless.disabled = False
            self.ids.btn_colorless.opacity = 1
            self.ids.btn_colorless.pos_hint = {'x': 0.7, 'y': 0.3}
            self.ids.lab_colorful_text.opacity = 1
            self.ids.lab_colorful_text.pos_hint = {'x': 0.4625, 'y': 0.125}
            self.ids.btn_colorless_text.opacity = 1
            self.ids.btn_colorless_text.pos_hint = {'x': .7025, 'y': .125}
            self.ids.kb.opacity = 0
            self.ids.slider_all.text = ' / 1'
            self.ids.kb.disabled = True
            self.ids.kb_pos.opacity = 0
            self.ids.kb_pos.disabled = True
            self.ids.imageView.source = 'pages/kv/assets/images/loader_1.gif'
            self.ids.loading_text.opacity = 1
            self.ids.imageView.reload()
            self.check_duplex('')
            self.ids.One_side.color = 1, 1, 1, 1
            self.ids.Two_side.color = .3, .3, .3, 1
            self.ids.Side_Chooser.pos_hint = {'x': .465, 'y': .2125}
            self.check_orientation('portrait')
            self.ids.Vertical.color = 1, 1, 1, 1
            self.ids.Horizontal.color = .3, .3, .3, 1
            self.ids.Orientation_Chooser.pos_hint = {'x': .72, 'y': .2125}
            self.color_choose('-color')

            self.pic_reloaded = 0

            CLOUD_PRINT.reset()
            CLOUD_PRINT.reset_timer()
            CLOUD_PRINT.clear_document_name()
            CLOUD_PRINT.reset_file_type()
            CLOUD_PRINT.clear_total_page()

            printing_popup = PrintingPopup()
            printing_popup.timer()
            printing_popup.open()

        else:
            # TODO хуудасны тоог вебээс авахад алдаа гарлаа!
            print(data)

    def cash_calculator(self, *args):
        """
            Хэрэглэгчийн файлын мөнгөн дүнг бодох хэсэг
        """

        color_value = CLOUD_PRINT.get_color_value()
        copies_number = CLOUD_PRINT.get_copies_number()
        page_chooser_value = CLOUD_PRINT.get_page_chooser_value()
        page_input_value = CLOUD_PRINT.get_page_input_value()
        paper_duplex = CLOUD_PRINT.get_paper_duplex()

        if color_value == "-color":
            CLOUD_PRINT.color_type_change('colored')
            price = 325
        else:
            CLOUD_PRINT.color_type_change('mono')
            # price = 175
            price = 10

        if paper_duplex == '-duplex':
            CLOUD_PRINT.req_duplex_change(True)
        else:
            CLOUD_PRINT.req_duplex_change(False)

        if page_chooser_value is True:
            total_cash = str(CLOUD_PRINT.get_total_page() * price * copies_number)
            CLOUD_PRINT.total_cash_change(total_cash)
            CLOUD_PRINT.printed_page_change(CLOUD_PRINT.get_total_page())
        else:
            To_array = page_input_value.split(",")
            counter = 0
            for i in To_array:
                if i.find("-") != -1:
                    save_array = i.split("-")
                    counter = (int(save_array[1]) - int(save_array[0])) + 1
                else:
                    counter += 1
            total_cash = str(counter * price * copies_number)
            CLOUD_PRINT.total_cash_change(total_cash)
            CLOUD_PRINT.printed_page_change(counter)
        self.ids.CashAmount.text = total_cash

    def PosMachine(self):
        QsPops = PosMachine_Popup(self)
        QsPops.open()

    def Loading_Popup(self):
        LPops = Loading_Popup(self)
        LPops.open()

    def payment_pp(self):
        PayPops = Payment_Popup(self)
        PayPops.open()

    def loading_continue_pp(self):
        LCPops = Loading_Continue_Popup(self)
        LCPops.open()

    def Loading_direct_print_PP(self):
        LDPops = Loading_Direct_Print_Popup(self)
        LDPops.open()

    def check_left_paper(self):
        if (CLOUD_PRINT.get_printed_page() > CLOUD_PRINT.get_printer_paper() - 10):
            self.caution_pp()
        else:
            self.loading_continue_pp()

    def _direct_print_PP(self):
        DPrint = DirectPrint_Popup(self)
        DPrint.open()

    def social_pay_pp(self):
        SPay = SocialPay_Popup(self)
        SPay.open()

    def QPAY_PP(self):
        QPAY = QPAY_Popup(self)
        QPAY.open()

    def caution_pp(self):
        Caution = CheckLeftPaperPopup()
        Caution.open()
    pass
