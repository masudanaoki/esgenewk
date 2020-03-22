import json
import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder


class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, InMemoryUploadedFile):
           return o.read()
        return str(o)


class CustomJson():
    def truns(dict_):
        return json.dumps(dict_, cls=CustomJsonEncoder)


if __name__=='__main__':
    path ='/'.join([os.path.dirname(__file__), 'json.jpg'])
    with open(path, 'rb') as f:
        file_ = f.read()
        dict_ = {'doc_file': file_}
        upload_file_data = CustomJson.truns(dict_)
