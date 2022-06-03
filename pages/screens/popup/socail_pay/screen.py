import os
import qrcode

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup

from settings.configuration import KIOSK
from cloudPrint.cloud_print import CLOUD_PRINT
from urls.socialPay.social_pay import socialpay_request
from urls.socialPay.social_pay import socialpay_check_payment

from utils.sound.sounds import success_sound


Builder.load_file('pages/kv/popup/social_pay/main.kv')


class SocialPay_Popup(Popup):

    def __init__(self, obj, **kwargs):
        super(SocialPay_Popup, self).__init__(**kwargs)
        self.obj = obj
        self.color_value = CLOUD_PRINT.get_color_value()
        self.paper_duplex = CLOUD_PRINT.get_paper_duplex()
        self.printed_page = CLOUD_PRINT.get_printed_page()
        self.total_cash = CLOUD_PRINT.get_total_cash()
        self.color_type = CLOUD_PRINT.get_color_type()
        self.req_duplex = CLOUD_PRINT.get_req_duplex()

        self.socialpay_data = ''
        self.ids.Pay_Amount.text = self.total_cash + " MNT"
        Clock.schedule_once(self.SocialPay_Request, 1)
        Clock.schedule_interval(self.TimeCounter, 1)
        self.ids.CopyNum.text = str(CLOUD_PRINT.get_copies_number())
        self.ids.PageNum.text = str(self.printed_page)

        if self.color_value == "-color":
            self.ids.PageColor.text = "Өнгөт"
            self.color_paper_price = 325
            self.ids.PageColor_price.text = str(self.color_paper_price)
        else:
            self.ids.PageColor.text = "Хар"
            self.black_paper_price = 175
            self.ids.PageColor_price.text = str(self.black_paper_price)

        if self.paper_duplex == '-duplex':
            self.ids.PageSide_price.text = "2"
        else:
            self.ids.PageSide_price.text = "1"

    def SocialPay_Request(self, *args):
        # -------------------------------------QR REQUEST----------------------------------------------
        body = {
            "printerId": KIOSK.get('id'),
            "amount": str(self.total_cash),
            "color_type": self.color_type,
            "pages": str(self.printed_page),
            "side": self.req_duplex,
        }
        # QR_json = {"printerId": SetVariables.get_id(), "amount": '1', "color_type": self.color_type, "pages": str(self.printed_page), "side": self.req_duplex}
        rsp_success, data = socialpay_request(body)
        if not rsp_success:
            self.ids.SocialPay_Caption.text = "АЛДАА ГАРЛАА. ДАХИН ОРОЛДОНО УУ"
            self.ids.SocialPay_QR.source = 'pages/kv/popup/social_pay/images/Error.png'

        self.socialpay_data = data
        img = qrcode.make(self.socialpay_data['qrCode']['body']['response']['desc'])
        img.save('cloudPrint/asset/socialPay/' + str(self.socialpay_data['invoice']) + '.png')
        # TODO log бичдэг байх!
        # LogWrite.success_log("SocialPay", self.socialpay_data['invoice'])
        Clock.schedule_interval(self.check_qr, 1)

    def check_qr(self, *args):
        # NOTE Зураг байхгүй бол яах вэ?
        if os.path.exists('cloudPrint/asset/socialPay/' + str(self.socialpay_data['invoice']) + '.png'):
            self.ids.SocialPay_QR.source = 'cloudPrint/asset/socialPay/' + str(self.socialpay_data['invoice']) + '.png'
            self.ids.SocialPay_Caption.text = "ТА ДАРААХ QR КОДЫГ УНШУУЛНА УУ"
            Clock.schedule_interval(self.check_payment, 5)
            Clock.unschedule(self.check_qr)

    def check_payment(self, *args):
        body = {'invoice': self.socialpay_data['invoice']}
        is_success, data = socialpay_check_payment(body)

        # TODO log бичдэг болгох!
        # LogWrite.send_invoice(self.socialpay_data['invoice'])
        # NOTE response байхгүй бол яах вэ?
        if is_success:
            payment_response = data
            if payment_response['resp_code'] == '00':
                self.ids.SocialPay_Caption.text = "ГҮЙЛГЭЭ АМЖИЛТТАЙ ХИЙГДЛЭЭ"
                self.ids.SocialPay_Caption.color = 0.12, 0.81, 0.35, 1
                self.ids.SocialPay_QR.source = 'cloudPrint/asset/success.png'
                success_sound()
                self.ids.SocialPay_QR.size_hint = .55, .4
                self.ids.SocialPay_QR.pos_hint = {'x': .48, 'y': .3}
                # TODO энд дуудах биш тухайн class дээр нь дуудах
                Clock.schedule_once(self.obj._print_service, 2)
                Clock.schedule_once(self.stopCheckPayment, 2)
                # TODO худалдан авалт амжилттай гэсэн log бичих!
                # LogWrite.payment_success(self.socialpay_data['invoice'])
            else:
                self.socialpay_data = ''

        else:
            print('QPay-ийн хүсэлтийг шалгаад алдаа гарсан')

    def TimeCounter(self, *args):
        counter = int(self.ids.time_counter.text)
        counter -= 1
        self.ids.time_counter.text = str(counter)
        if counter <= 0:
            self.stopCheckPayment()

    def stopCheckPayment(self, *args):
        Clock.unschedule(self.SocialPay_Request)
        Clock.unschedule(self.check_payment)
        Clock.unschedule(self.TimeCounter)
        Clock.unschedule(self.check_qr)
        if self.socialpay_data != "":
            os.remove('CloudPrint/asset/SocialPay/' + str(self.socialpay_data['invoice']) + '.png')
        self.socialpay_data = ''
        self.dismiss()
