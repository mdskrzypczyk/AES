from cipher import Cipher

def main():
    iv = [0]*16
    key = "0123456789abcdef0123456789abcdef"
    plaintext = 'the dog jumps!!!'
    cipher = Cipher(iv=iv, key=key)
    cipher.expand_key()
    ciphertext = cipher.encrypt(plaintext)
    cipherbytes = [ord(c) for c in ciphertext]
    print("Output: " + ''.join(ciphertext))
    plaintext = cipher.decrypt(ciphertext)
    print("Decrypted: " + ''.join(plaintext))
    

if __name__ == '__main__':
    main()
