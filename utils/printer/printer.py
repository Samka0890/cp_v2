import win32api
import win32print

from settings.configuration import GSPRINT_PATH
from settings.configuration import GHOSTSCRIPT_PATH

from cloudPrint.cloud_print import CLOUD_PRINT


def printing(page_num_start, page_num_end):

    current_printer = win32print.GetDefaultPrinter()

    file_name = CLOUD_PRINT.get_document_name()

    gsprint_path = CLOUD_PRINT.get_base_dir() + GSPRINT_PATH
    ghostscript_path = CLOUD_PRINT.get_base_dir() + GHOSTSCRIPT_PATH

    copies_number = CLOUD_PRINT.get_copies_number()
    color_value = CLOUD_PRINT.get_color_value()
    paper_duplex = CLOUD_PRINT.get_paper_duplex()
    page_orientation = CLOUD_PRINT.get_page_orientation()

    print(file_name)

    params = """-ghostscript "{ghostscript_path}" -printer "{current_printer}" "{file_name}"
    """.format(
        ghostscript_path=ghostscript_path,
        current_printer=current_printer,
        file_name=file_name,
        page_num_start=page_num_start,
        page_num_end=page_num_end,
        page_orientation=page_orientation,
        paper_duplex='"' + paper_duplex + '"' if paper_duplex else '',
        copies_number=copies_number,
        color_value=color_value,
    )

    win32api.ShellExecute(
        0,
        'open',
        gsprint_path,
        str(params),
        '.',
        0
    )

    print('done')
