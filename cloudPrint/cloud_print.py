import os

from cloudPrint.user.user_file import FileType
from cloudPrint.user.user_file import UserDocPath
from cloudPrint.user.user_file import UserPageInfo
from cloudPrint.user.user_file import FileConvertTimer

from cloudPrint.user.user_timer import UserTimer
from cloudPrint.user.printing import Printing

from cloudPrint.page.previous_page import PreviousPage
from cloudPrint.driver.driver_logout import DriverLogout

from cloudPrint.qr.qr import QrReader

from cloudPrint.printer.printer import Printer

from urls.fileRequest.file_request import FileRequest


class CloudPrint(
    FileType,
    UserDocPath,
    UserPageInfo,
    FileConvertTimer,

    UserTimer,

    Printing,

    PreviousPage,
    DriverLogout,

    QrReader,

    Printer,

    FileRequest,
):

    def __init__(self, **kwargs):
        super(CloudPrint, self).__init__(**kwargs)
        self.base_dir = os.getcwd()

    # ------------------------ BASE_DIR ------------------------
    def get_base_dir(self):

        return self.base_dir


CLOUD_PRINT = CloudPrint()
