import os
from urllib.parse import urlparse, unquote


def get_file_extension(url):
    url = unquote(url)
    path = urlparse(url).path
    head, tail = os.path.split(path)
    root, extension = os.path.splitext(tail)
    return extension
