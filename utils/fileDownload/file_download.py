import os

from cloudPrint.cloud_print import CLOUD_PRINT


def download_file(resp):
    # TODO файлын өргөтгөлийг шинэчлэх!

    is_downloaded = False
    download_type = resp.headers['content-type'].split('/')

    if download_type[1].lower() == 'pdf':
        # type.SetFileType('pdf')
        # TODO файлын өргөтгөлийг pdf болгох!

        file_dir = os.path.join(CLOUD_PRINT.get_base_dir(), 'cloudPrint/downloadedFile/downloadFile.pdf')
        with open(file_dir, 'wb') as f:
            f.write(resp.content)

        f.close()

        file_dir = 'cloudPrint/downloadedFile/downloadFile.pdf'
        CLOUD_PRINT.set_document_name(file_dir)

        # NOTE файл амжилттай татагдсан гэсэн үг!
        is_downloaded = True
    # else:
    #     type.SetFileType('docx')
    #     fileDir = 'CloudPrint/DownloadFile/downloadFile.doc'
    #     with open(fileDir, 'wb') as f:
    #         f.write(resp.content)
    #     f.close()
    #     fileDir = ['CloudPrint/DownloadFile/downloadFile.doc']
    #     CLOUD_PRINT.set_document_name(fileDir)

    return is_downloaded
