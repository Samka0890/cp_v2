import os
from datetime import timedelta
from timeit import default_timer as timer

from PyPDF2 import PdfFileReader

from kivy.loader import Loader

base_dir = os.getcwd()


class UserDocPath:
    """
        Хэрэглэгчийн файлтай холбоотой class
    """

    filename = ''

    def get_document_name(self):
        """
            UserDocPath object-ээс хэрэглэгчийн файлын нэрийг авах функц
        """

        return self.filename

    def set_document_name(self, file_name):
        """
            UserDocPath object-ийн хэрэглэгчийн файлын нэрийг солих функц
        """

        if file_name:
            self.filename = file_name
        elif file_name == '':
            self.filename = ''

    def clear_document_name(self):
        """
            UserDocPath object-ийн хэрэглэгчийн файлын нэрийг солих функц
        """

        self.filename = ''


class FileType:
    type = ''

    def extract_file_type(self, file_name):
        splited_name = file_name.split(".")
        file_type = splited_name[-1].lower()
        # TODO xlsx, txt
        if file_type == 'pdf' or file_type == 'doc' or file_type == 'docx':
            self.type = file_type
            return False
        else:
            return True

    def get_file_type(self):

        return str(self.type)

    def set_file_type(self, file_type):
        self.type = file_type.lower()

    def reset_file_type(self):
        """Файлын төрлийг анхны төлөвд оруулах"""

        self.type = ''


class FileConvertTimer:
    """
        Хэрэглэгчийн файлыг зурган файл болгоход зарцуулагдах хугацааг агуулах хувьсагч
    """
    timer = ''
    start_time = ''
    end_time = ''

    def file_conv_start(self):
        """
            FileType object-ээс хэрэглэгчийн файлын нэрийг авах функц
        """

        self.start_time = timer()

    def file_conv_end(self):
        self.end_time = timer()
        self.set_timer_duration(timedelta(seconds=self.end_time-self.start_time))

    def get_timer_duration(self):
        """
            FileType object-аас хэрэглэгчийн файлын өргөтгөлийг авах функц
        """

        return self.timer

    def set_timer_duration(self, set_duration):
        """
            FileType object-ийн хэрэглэгчийн файлын өргөтгөлийг солих функц
        """

        self.timer = set_duration

    def reset_timer(self):
        """
            FileType object-ийн хэрэглэгчийн файлын нэрийг солих функц
        """

        self.timer = 0


class UserPageInfo:
    total_page = 1

    # get
    def get_total_page(self):
        return self.total_page

    def set_page_from_file(self, file_name):
        f = open(file_name, 'rb')
        pdf = PdfFileReader(f)
        self.set_total_page(pdf.getNumPages())
        Loader.start()
        f.close()

    # setter method
    def set_total_page(self, page_num):
        self.total_page = page_num

    def clear_total_page(self):
        """Хуудасны тоо анхны төлөвд оруулах"""

        self.total_page = 1


def check_file_corrupted(file_type, path):
    # TODO validation хийх
    return False

    path = path[0]

    if ' ' in path:
        path = '"' + path + '"'


    if file_type == 'pdf':
        validator_path = base_dir + '\\CloudPrint\\pdfvalidator\\PDFValidator.exe '
        os.system(validator_path + path)
        f = open('pdfvalidator.txt', 'r')
        checker = f.readline().rstrip()
        f.close()
        if checker == "0":
            return True
        else:
            return False
    elif file_type == 'docx':
        validator_path = base_dir + '\\CloudPrint\\docx_validator\\WordValidator.exe '
        os.system(validator_path + path)
        f = open('write.txt', 'r')
        checker = f.readline().rstrip()
        f.close()
        if checker == "0":
            return True
        else:
            return False
    else:
        return False
