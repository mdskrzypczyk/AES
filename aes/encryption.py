from aes_operations import *

class Encryption:
    def __init__(self, block, key, key_size):
        #Want to save message length in case we need to pad with 0's
        self.message_length = len(block)
        self.message = ''

        block = append_length(block)
        #Pad message with 0's until a proper multiple of 32 reached
        while len(block) % 32 != 0:
            block += '0'

        #Change number of rounds based on size of key
        if key_size == 16:
            num_rounds = 10
        elif key_size == 24:
            num_rounds = 12
        elif key_size == 32:
            num_rounds = 14

        #Variable to keep track of where we are in the message
        block_start = 0
        #Perform encryption
        for encryptions in range(len(block)/32):

            #First Add Round Key
            current_message_section = add_round_key(key[0:32], block[block_start:block_start+32])
            #Iterate for the rounds that do the same thing
            for encryption_round in range(1, num_rounds):
                current_message_section = add_round_key(key[encryption_round*32:(encryption_round+1)*32], mix_column(shift_row(byte_sub(current_message_section))))

            #Final round of add round key, shift row, and byte substitution
            current_message_section = add_round_key(key[num_rounds*32:(num_rounds+1)*32], shift_row(byte_sub(current_message_section)))
            
            #Append the encrypted block onto the message
            self.message += current_message_section

            #Increment section of message we are encrypting
            block_start += 32
