import os
import threading

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder

from cloudPrint.cloud_print import CLOUD_PRINT
from cloudPrint.user.user_file import check_file_corrupted

from urls.connectionStatus.urls import web_working

from pages.screens.popup.internetConnectionError import screen as net_conn_screen

from settings.global_variables import USER_TIME

from settings.configuration import IS_UBUNTU
from settings.configuration import COM_USER_NAME

from utils.file.file import pdf_to_image
from utils.sound.sounds import click_sound
from utils.folder.folder import reset_folder

CHECKER_VARIABLE = ['.DS_Store']

Builder.load_file('pages/kv/offline/main.kv')


class OfflineScreen(Screen):
    default_flash_path = 'cloudPrint/flash'
    flash_path = default_flash_path

    def __init__(self, **kwargs):
        super(OfflineScreen, self).__init__(**kwargs)
        self.check_flash_finished = False

    def sw_timer(self, *args):
        if self.parent is not None:
            self.parent.transition.direction = 'right'
            self.parent.current = "main_screen"
            Clock.unschedule(self.sw_timer)

    def on_enter(self, *args):
        if web_working():
            # NOTE хуудас шилжих хэсэг
            Clock.schedule_interval(self.sw_timer, 15)
            Clock.schedule_interval(self.usb_timer, 1)

            # NOTE хуудасны утгыг тохируулах хэсэг
            CLOUD_PRINT.set_previous_page('offline_screen')

            # NOTE хуудасны шилжүүлэх хугацааг тохируулах хэсэг
            CLOUD_PRINT.get_user_timer()
        else:
            net_conn_err_poppup = net_conn_screen.InternetConnectionError()
            net_conn_err_poppup.open()

    def refresh(self, *args):
        self.ids.filechooser.rootpath = self.flash_path
        self.ids.filechooser._update_files()

    def usb_timer(self, *args):
        if IS_UBUNTU:
            # NOTE ubuntu дээр flash болон disk-үүд media дотор орж ирдэг
            root_path = os.path.join('/media', COM_USER_NAME)
            check_aviable_drives = os.listdir(root_path)
            if check_aviable_drives and len(check_aviable_drives) > 0:
                flash_path = os.path.join(root_path, check_aviable_drives[0])
                self.flash_path = flash_path
                files = os.listdir(flash_path)
                if files and CLOUD_PRINT.get_driver_log_out() is True:
                    CLOUD_PRINT.set_driver_log_out(False)
                    self.ids.loader.opacity = 1
                    self.ids.loader_text.opacity = 1
                    self.check_flash()
                    # self.threading = threading.Thread(target=self.check_flash)
                    # self.threading.start()
                    self.check_flash_finished = False
                    Clock.schedule_interval(self.check_flash_finish, 1)
                    Clock.unschedule(self.usb_timer)
                    Clock.schedule_interval(self.usb_logout, 1)
                    Clock.unschedule(self.sw_timer)
            else:
                self.flash_path = self.default_flash_path
        else:
            # NOTE windows дээр flash болон disk-ийг авахад ашиглах
            check_aviable_drives = [chr(x) + ":/" for x in range(65, 90) if os.path.exists(chr(x) + ":/")]
            if check_aviable_drives and len(check_aviable_drives) != 1:
                self.flash_path = str(check_aviable_drives[-1])
                files = os.path.exists(self.flash_path)
                if files and CLOUD_PRINT.get_driver_log_out() is True:
                    CLOUD_PRINT.set_driver_log_out(False)
                    self.ids.loader.opacity = 1
                    self.ids.loader_text.opacity = 1
                    self.check_flash()
                    # self.threading = threading.Thread(target=self.check_flash)
                    # self.threading.start()
                    self.check_flash_finished = False
                    Clock.schedule_interval(self.check_flash_finish, 1)
                    Clock.unschedule(self.usb_timer)
                    Clock.schedule_interval(self.usb_logout, 1)
                    Clock.unschedule(self.sw_timer)
            else:
                self.flash_path = self.default_flash_path

    def check_flash_finish(self, *args):
        if self.check_flash_finished is False:
            self.refresh()
            Clock.unschedule(self.check_flash_finish)

    def check_flash(self):
        # folder_name = 'driveScan'
        # reset_folder(folder_name)

        # TODO Kaspersky хийх
        # cmd = r'"C:\Program Files (x86)\Kaspersky Lab\Kaspersky Anti-Virus 21.3\avp.com" SCAN /remdrives /i0 -e:5 -es:10 /R:"C:\CP\CloudPrint\drive_scan\result.txt"'
        # subprocess.call(cmd, shell=True)

        # TODO ubuntu дээр virus шалгах арга https://www.linuxcapable.com/how-to-install-and-use-clamav-on-ubuntu-20-04/

        self.ids.loader.opacity = 0
        self.ids.loader_text.opacity = 0
        detected = 0
        # f = open('Cloudprint/drive_scan/result.txt')
        # resultTxt = f.readlines()
        # for line in resultTxt:
        #     if ('Total detected' in line):
        #         detected = int(''.join(filter(str.isdigit, line)))

        if detected == 0:
            self.ids.WarningText.text = "Файлаа сонгоно уу!"
            self.ids.filechooser.disabled = False
        else:
            self.ids.WarningText.text = "Таны төхөөрөмж вирустэй байна.\n             Дахин оролдоно уу."
            self.ids.filechooser.disabled = True

        self.check_flash_finished = True

    def usb_logout(self, *args):
        files = os.path.exists(self.flash_path)
        if files is False:
            CLOUD_PRINT.set_driver_log_out(True)
            self.ids.loader.opacity = 0
            self.ids.loader_text.opacity = 0
            Clock.schedule_interval(self.sw_timer, 15)
            Clock.unschedule(self.usb_logout)
            self.flash_path = self.default_flash_path
            self.refresh()
            Clock.schedule_interval(self.usb_timer, 1)
            self.ids.WarningText.text = "Төхөөрөмжөө оруулна уу!"

    def chk_dev(self, file_names):
        click_sound()
        files = os.path.exists(self.flash_path)
        if files is True:
            files = os.listdir(self.flash_path)
            if files != CHECKER_VARIABLE:
                if file_names:
                    CLOUD_PRINT.set_document_name(file_names[0])
                    CLOUD_PRINT.extract_file_type(file_names[0])
                    rsp_file_cop = check_file_corrupted(CLOUD_PRINT.get_file_type(), file_names)
                    if rsp_file_cop is False:
                        self.ids.WarningText.text = "Үргэлжлүүлэх үү?"
                        self.ids.btn1.opacity = 1
                        self.ids.btn2.opacity = 1
                        self.ids.btn1.disabled = False
                        self.ids.btn2.disabled = False
                        self.ids.opLbl_true.opacity = 0
                        self.ids.opLbl_false.opacity = 0
                        self.ids.opLbl_true.opacity = 1
                        self.ids.opLbl_false.opacity = 1
                    else:
                        self.ids.WarningText.text = "Уучлаарай. Таны файл алдаатай байна.\n Файлаа шинэчлээд дахин оролдоно уу."
                else:
                    self.ids.WarningText.text = "Файлаа сонгоно уу!"
            else:
                self.ids.WarningText.text = "Төхөөрөмжөө оруулна уу!"
        else:
            self.ids.WarningText.text = "Төхөөрөмжөө оруулна уу!"

    def del1(self):
        click_sound()
        self.ids.WarningText.text = "Төхөөрөмжөө оруулна уу!"
        self.ids.btn1.opacity = 0
        self.ids.btn2.opacity = 0
        self.ids.btn1.disabled = True
        self.ids.btn2.disabled = True
        self.ids.opLbl_true.opacity = 0
        self.ids.opLbl_false.opacity = 0

    def check_str(self, *args):
        if args != []:
            self.ids.btn1.opacity = 0
            self.ids.btn2.opacity = 0
            self.ids.btn1.disabled = True
            self.ids.btn2.disabled = True
            self.ids.opLbl_true.opacity = 0
            self.ids.opLbl_false.opacity = 0
            self.ids.WarningText.text = "Файлаа сонгоно уу!"
            file_name = args[1]
            file_name = args[1]
            choose_btn = True
            if file_name:
                file_name = file_name[0]
                choose_btn = CLOUD_PRINT.extract_file_type(file_name)

            self.ids.save.disabled = choose_btn

    def set_configure(self):
        # TODO шалгах
        # if CLOUD_PRINT.get_file_type() == 'pdf':
        #     t0 = threading.Thread(target=FileFixing)
        #     t0.start()
        CLOUD_PRINT.set_on_print_page(True)

        t1 = threading.Thread(target=self.set_page())
        t2 = threading.Thread(target=file_convert())
        # t1.start()
        # t2.start()

    def set_page(self):
        self.parent.transition.direction = 'left'
        self.parent.current = 'print_screen'
        self.parent.ids.print_screen.imageView.source = 'pages/kv/assets/images/loader_1.gif'
        self.parent.ids.print_screen.imageView.reload()
        self.parent.ids.print_screen.rightButton.disabled = True
        self.parent.ids.print_screen.leftButton.disabled = True
        self.parent.ids.print_screen.slider.disabled = True

    pass


def file_convert():
    CLOUD_PRINT.file_conv_start()
    file_path = CLOUD_PRINT.get_document_name()
    if CLOUD_PRINT.get_file_type() == 'pdf':
        CLOUD_PRINT.set_page_from_file(file_path)
        pdf_to_image(file_path, 50)
        if CLOUD_PRINT.get_on_print_page() is True:
            CLOUD_PRINT.file_conv_end()

    else:
        # TODO doc to pdf
        print('DOC TO PDF')
        pass

    # TODO gswin32 ажиллуулах
#     inputpath = str(UsrPathOb.getDocumentName())
#     ConvertTimer.start()
#     if UsrFileType.GetFileType() == 'pdf' or UsrFileType.GetFileType() == 'PDF':
#         UserPageInfo.set_page_from_file(inputpath)
#         pdf2image(inputpath, 50, PreviousPage)
#         if PreviousPage.get_on_print_page() is True:
#             ConvertTimer.end()
# # -------------------------------------------DOC File Read-------------------------------------------------------------------
#     elif UsrFileType.GetFileType() == 'docx' or UsrFileType.GetFileType() == 'doc' or UsrFileType.GetFileType() == 'DOCX' or UsrFileType.GetFileType() == "DOC":
#         sample_doc = UsrPathOb.getDocumentName()
#         out_folder = 'CloudPrint/save_docx'
#         GhostWorking.set_office_status(False)
#         os.system('C:/CP/CloudPrint/OfficeToPDF/OfficeToPDF.exe /bookmarks /print /verbose "' + sample_doc + '" CloudPrint/save_docx/convert_pdf.pdf')
#         GhostWorking.set_office_status(True)
#         UsrPathOb.setDocumentName(['CloudPrint/save_docx/convert_pdf.pdf'])
#         DataString = str(os.path.basename(UsrPathOb.getDocumentName())).rsplit(".", 1)
#         ConvertName = str(out_folder + '/' + DataString[0] + '.pdf')
#         FileName = ConvertName
#         fileNameError = ConvertName.find(" ")

#         if PreviousPage.get_on_print_page() is True:
#             UserPageInfo.set_page_from_file(FileName)
#             inputpath = FileName
#             pdf2image(inputpath, 60, PreviousPage)
#             ConvertTimer.end()

#         if fileNameError != -1:
#             newPath = ConvertName.replace(' ', '_')
#             FileName = newPath
#             os.replace(str(ConvertName), newPath)

#         if PreviousPage.get_on_print_page() is True:
#             GhostWorking.set_status(False)
#             os.system('C:/CP/CloudPrint/GHOSTSCRIPT/bin/gswin32c.exe -o outputA6.pdf -sDEVICE=pdfwrite -sPAPERSIZE=a4 -dFIXEDMEDIA -dDEVICEWIDTHPOINTS=595 -dDEVICEHEIGHTPOINTS=790 -dPDFFitPage -dCompatibilityLevel=1.3 -c 60000000 setvmthreshold -f' + ' ' + FileName)
#             GhostWorking.set_status(True)
