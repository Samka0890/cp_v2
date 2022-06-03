import os
from pdf2image import convert_from_path

from cloudPrint.cloud_print import CLOUD_PRINT


# NOTE pdf-ээс зураг руу хөрвүүлсэн зургуудыг хадгалах folder
base_dir = CLOUD_PRINT.get_base_dir()
img_save_path = "cloudPrint/save_image/image"

root_save_path = os.path.join(base_dir, img_save_path)


def pdf_to_image(input_path, convert_size=50):
    pages = convert_from_path(input_path, convert_size)
    for i, page in enumerate(pages):
        if CLOUD_PRINT.get_on_print_page() is True:
            # TODO folder байхгүй бол яах вэ?
            fname = root_save_path + str(i) + ".png"
            page.save(fname, "png")
        else:
            return False
    return True
