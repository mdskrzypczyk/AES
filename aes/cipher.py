import base64
from aes_lib import *

class Cipher:
    def __init__(self, mode='ECB', iv=None, key=None):
        self.mode = mode
        self.expanded_key = key
        self.iv = iv

    def expand_key(self):
        # Transform into a byte array
        self.expanded_key = [ord(b) for b in self.expanded_key.decode('hex')]

        # Check length
        if len(self.expanded_key) in VALID_KEY_LENGTHS:
            self.expanded_key = expand_key(self.expanded_key)
            return self.expanded_key

        else:
            print("Invalid key specified")
            raise

    def encrypt(self, plaintext):
        # ECB mode
        ciphertext = []
        padded_plaintext = pad_plaintext(plaintext)
        print(padded_plaintext)
        plaintext_blocks = plaintext_to_blocks(padded_plaintext)
        iv = [0] * 16

        for block in plaintext_blocks:
            ciphertext += encrypt_block(iv, block, self.expanded_key)

        ciphertext = [chr(c) for c in ciphertext]
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = []
        ciphertext = [ord(c) for c in ciphertext]
        ciphertext_blocks = [ciphertext[i:i+AES_BLOCK_SIZE] for i in range(0, len(ciphertext), AES_BLOCK_SIZE)]
        iv = [0] * 16

        for block in ciphertext_blocks:
            plaintext += decrypt_block(iv, block, self.expanded_key)

        padding_num = plaintext[-1]
        plaintext = plaintext[0:len(plaintext) - (padding_num+1)]
        plaintext = [chr(p) for p in plaintext]
        return plaintext
