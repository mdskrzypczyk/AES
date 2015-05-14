from aes_operations import *

class Decryption:
    def __init__(self, block, key, key_size):
        #Want to save message length in case we need to pad with 0's
        self.message_length = len(block)
        self.message = ''

        #Change number of rounds based on size of key
        if key_size == 16:
            num_rounds = 10
        elif key_size == 24:
            num_rounds = 12
        elif key_size == 32:
            num_rounds = 14

        #Variable to keep track of where we are in the message
        block_start = 0
        key_start = len(key)-32

        #Perform encryption
        for decryptions in range(len(block)/32):
            #First Add Round Key
            current_key = key_start
            current_message_section = add_round_key(key[key_start:], block[block_start:block_start+32])
            current_key -= 32

            #Iterate for the rounds that do the same thing
            for encryption_round in range(1, num_rounds):
                current_message_section = imix_column(add_round_key(key[current_key:current_key+32], ibyte_sub(ishift_row(current_message_section))))
                current_key-= 32

            #Final round of add round key, shift row, and byte substitution
            current_message_section = add_round_key(key[0:32], ibyte_sub(ishift_row(current_message_section)))
            #Append the encrypted block onto the message
            self.message += current_message_section

            #Increment section of message we are encrypting
            block_start += 32

        #Remove length padding on message
        message_length = int(self.message[0:32],16)
        self.message = self.message[32:32+message_length]
