import base64
import mimetypes
import os
import shutil

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile


class CustomFile():
    def localfile_to_filefield(file_):
        with open(file_, 'rb') as f:
            mime = mimetypes.guess_type(file_)
            fileimage = SimpleUploadedFile(f.name, bytes(f.read()), content_type=mime[0])
            return fileimage

    def remove_dir(dir_):
        if default_storage.exists(dir_):
            return shutil.rmtree(dir_)

    def save_file(file_name, file_data):
        save_file = default_storage.save(file_name, file_data)
        return (default_storage.url(save_file), default_storage.path(save_file))


if __name__=='__main__':
    path ='/'.join([os.path.dirname(__file__), 'json.jpg'])
    dict_ = CustomFile.localfile_to_filefield(path)
