import base64
from aes_lib import *

class Cipher:
    def __init__(self, mode='ECB', key=None):
        self.mode = mode
        self.key = key

    def expand_key(self):
        pass

    def encrypt(self):
        pass

    def decrypt(self):
        pass
