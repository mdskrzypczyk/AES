import base64
from aes_lib import *

class Cipher:
    def __init__(self, mode='ECB', iv=None, key=None):
        self.mode = mode
        self.expanded_key = key
        self.iv = iv

    def expand_key(self):
        # Transform into an int array TODO: Implement smarter key format detection and conversion
        self.expanded_key = [ord(c) for c in self.expanded_key]

        # Check length
        if len(self.expanded_key) == 16:
            self.expanded_key = expand_key_128_192(self.expanded_key)
            return self.expanded_key
        elif len(self.expanded_key) == 24:
            self.expanded_key = expand_key_128_192(self.expanded_key)[:192]
            return self.expanded_key
        elif len(self.expanded_key) == 32:
            self.expanded_key = expand_key_256(self.expanded_key)
            return self.expanded_key
        else:
            print("Invalid key specified")
            raise

    def encrypt(self, plaintext):
        # ECB mode
        ciphertext = []
        padded_plaintext = pad_plaintext(plaintext)
        plaintext_blocks = plaintext_to_blocks(padded_plaintext)

        for block in plaintext_blocks:
            ciphertext += encrypt_block(self.iv, block, self.expanded_key)

        ciphertext = [chr(c) for c in ciphertext]
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = []
        ciphertext = [ord(c) for c in ciphertext]
        ciphertext_blocks = [ciphertext[i:i+AES_BLOCK_SIZE] for i in range(0, len(ciphertext), AES_BLOCK_SIZE)]

        for block in ciphertext_blocks:
            plaintext += decrypt_block(self.iv, block, self.expanded_key)

        padding_num = plaintext[-1]
        plaintext = plaintext[0:len(plaintext) - (padding_num)]
        plaintext = [chr(p) for p in plaintext]
        return plaintext
