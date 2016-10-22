import base64
import aes_lib

class Cipher:
    def __init__(self, mode='ECB', iv=None, key=None):
        self.mode = mode
        self.expanded_key = key
        self.iv = iv

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

    def encrypt(self, plaintext):
        # ECB mode
        plaintext = [ord(c) for c in plaintext]
        plaintext_blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]

        ciphertext = []
        iv = [0] * 16

        for block in plaintext_blocks:
            if len(block) < 16:
                block += [16-len(block)]*(16-len(block))

            ciphertext += aes_lib.encrypt_block(iv, block, self.expanded_key)

        return ciphertext

    def decrypt(self, ciphertext):
        pass
