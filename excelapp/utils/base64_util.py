import base64
import os


class CustomBase64():
    def encode_str(value_):
        return base64.b64encode(value_).decode("ascii")

    def decode(value_):
        return base64.b64decode(value_)


if __name__=='__main__':
    path ='/'.join([os.path.dirname(__file__), 'json.jpg'])
    with open(path, 'rb') as f:
        file_ = f.read()
        str_ = CustomBase64.encode_str(file_)
        byte_ = CustomBase64.decode(str_)

