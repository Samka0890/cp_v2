import os

base_dir = os.getcwd()


def reset_folder(folder_name):

    target_path = os.path.join(base_dir, folder_name)

    for file_name in os.listdir(target_path):
        if file_name != '.keep':
            os.unlink(os.path.join(target_path, file_name))


def checkfolder(folder_name):
    """
        Уг функцад fodler-ийн нэрээ өгнө
            Жишээ нь: cloudPrint/save_image/image
    """
    folder_path = os.path.join(base_dir, folder_name)

    return os.path.isdir(folder_path)
