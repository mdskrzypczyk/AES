import base64
import aes_lib

class Cipher:
    def __init__(self, mode='ECB', key=None):
        self.mode = mode
        self.expanded_key = key

    def expand_key(self):
        # Transform into a byte array
        self.expanded_key = [ord(b) for b in self.expanded_key.decode('hex')]

        # Check length
        if len(self.expanded_key) in aes_lib.VALID_KEY_LENGTHS:
            self.expanded_key = aes_lib.expand_key(self.expanded_key)
            return self.expanded_key
            
        else:
            print("Invalid key specified")
            raise

    def encrypt(self):
        pass

    def decrypt(self):
        pass
