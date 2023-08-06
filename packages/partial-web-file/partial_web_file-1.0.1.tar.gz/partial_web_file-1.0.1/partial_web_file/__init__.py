import io
import logging
import requests
import zipfile


log = logging.getLogger('partial_web_file')

SEEK_FROM_START = 0
SEEK_FROM_CURRENT_POSITION = 1
SEEK_FROM_END_OF_FILE = 2

DEFAULT_READ_CHUCK_SIZE = 1000000


def get_partial_web_file(url, start_position, length):
    headers = {"Range": "bytes=%d-%d" % (start_position, start_position + length - 1)}
    r = requests.get(url, headers=headers)
    data = r.content
    data_len = len(data)
    if data_len != length:
        log.warning('Web returned %d while asked only for %d... Does this Web server support the "Range" header?'
              % (data_len, length))
        return data[start_position:start_position + length]
    else:
        return data


class _RemoteStream(io.BytesIO):
    """
    Imitates the bytes stream while each request for the real data is gotten from the remote website resource.
    """
    def __init__(self, url):
        self._url = url
        self._cursor = 0

        with requests.get(self._url, stream=True) as r:
            self._length = int(r.headers['content-length'])
        if not self._length:
            raise Exception('Failed to get the length for resource ' + self._url)

    def seek(self, offset, whence=0):
        if whence == SEEK_FROM_START:
            self._cursor = offset
        elif whence == SEEK_FROM_CURRENT_POSITION:
            self._cursor += offset
        elif whence == SEEK_FROM_END_OF_FILE:
            self._cursor = self._length + offset
        else:
            raise ValueError("whence must be os.SEEK_SET (0), "
                             "os.SEEK_CUR (1), or os.SEEK_END (2)")

        if self._cursor > self._length:
            raise OSError("seek() position went over the size of a file")

        if self._cursor < 0:
            raise OSError("seek() position went below 0")

        return self.tell()

    def tell(self):
        return self._cursor

    def read(self, n=DEFAULT_READ_CHUCK_SIZE):
        count = min(n, self._length - self._cursor)
        data = get_partial_web_file(self._url, self._cursor, count)
        self._cursor += len(data)
        return data


def get_file_content_from_web_zip(zip_url, path_to_file_in_zip):
    stream = _RemoteStream(zip_url)
    with zipfile.ZipFile(stream, 'r') as zf:
        return zf.read(path_to_file_in_zip)
