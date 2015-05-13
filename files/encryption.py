sbox = open('files/sbox').read().replace('\n',' ' ).split(' ')

def add_round_key(current_key, state):
    #Perform XOR on invididual key and state bytes
    new_state = [int(a,16) ^ int(b,16) for a,b in zip(current_key,state)]

    #Turn it back into an ASCII representation
    new_state = ''.join([hex(a).replace('0x','') for a in new_state]).upper()
    return new_state

def byte_sub(state):
    new_state = ''

    #Perform sbox lookup and return substituted string
    for _ in range(0,len(state),2):
        new_state += sbox[int(state[_],16)*16 + int(state[_+1],16)]

    return new_state

def shift_row(state):
    #Separate state into individual "byte" ascii characters
    new_state = [state[_:_+2] for _ in range(0,len(state),2)]

    #Join every fourth character into it's own 'row' of the state
    first_row = ''.join(new_state[::4])
    second_row = ''.join(new_state[1::4])
    third_row = ''.join(new_state[2::4])
    fourth_row = ''.join(new_state[3::4])

    #Perform the byte shifts on each row
    second_row = second_row[2:] + second_row[0:2]
    third_row = third_row[4:] + third_row[0:4]
    fourth_row = fourth_row[6:] + fourth_row[0:6]

    #Reconstruct a state with the shifted rows
    ret_state = ''
    for _ in range(0,len(state)/2,2):
        ret_state += first_row[_:_+2]
        ret_state += second_row[_:_+2]
        ret_state += third_row[_:_+2]
        ret_state += fourth_row[_:_+2]

    return ret_state

def hex_mult(hex1, hex2):
    if hex2 == 2:
        #If leading bit is a 1 we need to XOR in addition to shift
        if hex1 >= int('80',16):
            hex1 = hex1 << 1
            hex1 ^= int('1B',16)
        else:
            hex1 = hex1 << 1

    #Multiplying by 3 is same as XORing hex1 with itself multiplied by 2
    elif hex2 == 3:
        hex1 = hex_mult(hex1,2) ^ hex1

    return hex1

def mix_column(state):
    #Basic multiplication matrix row, can reuse and shift
    mult_row = [2,3,1,1]

    #Separate state into individual 'byte' representation
    int_state = [state[_:_+2] for _ in range(0,len(state),2)]

    #Convert to integers to perform XOR
    int_state = [int(a,16) for a in int_state]

    new_state = []
    for _ in range(4):
        #Calculate each row byte
        bfirst = hex_mult(int_state[0], mult_row[0]) ^ hex_mult(int_state[1], mult_row[1]) ^ hex_mult(int_state[2], mult_row[2]) ^ hex_mult(int_state[3], mult_row[3])
        bsecond = hex_mult(int_state[4], mult_row[0]) ^ hex_mult(int_state[5], mult_row[1]) ^ hex_mult(int_state[6], mult_row[2]) ^ hex_mult(int_state[7], mult_row[3])
        bthird = hex_mult(int_state[8], mult_row[0]) ^ hex_mult(int_state[9], mult_row[1]) ^ hex_mult(int_state[10], mult_row[2]) ^ hex_mult(int_state[11], mult_row[3])
        bfourth = hex_mult(int_state[12], mult_row[0]) ^ hex_mult(int_state[13], mult_row[1]) ^ hex_mult(int_state[14], mult_row[2]) ^ hex_mult(int_state[15], mult_row[3])
        
        #If number is greater than 'FF' we need to remove the leading bit
        if bfirst > 255:
            bfirst -= 256
        if bsecond > 255:
            bsecond -= 256
        if bthird > 255:
            bthird -= 256
        if bfourth > 255:
            bfourth -= 256

        #Add these bytes to a list
        new_state.extend([bfirst, bsecond, bthird, bfourth])

        #Shift the multiplication row over for the next row of bytes
        mult_row = mult_row[3:] + mult_row[0:3]


    #Put the values back in correct order
    new_state = [new_state[_::4] for _ in range(4)]
    new_state = [num for _ in new_state for num in _]

    converted = []

    #When converting back to an ASCII representation, need to make sure digits less than 10 have a leading 0
    for item in new_state:
        if item < 10:
            converted.append('0'+hex(item).replace('0x',''))
        else:
            converted.append(hex(item).replace('0x',''))

    #Reconstruct the string
    new_state = ''.join(converted).upper()
    return new_state

class Encryption:
    def __init__(self, block, key, key_size):
        #Want to save message length in case we need to pad with 0's
        self.message_length = len(block)
        self.message = ''

        #Pad message with 0's until a proper multiple of 32 reached
        while len(block) % 32 != 0:
            block += '0'

        #Change number of rounds based on size of key
        if key_size == '16':
            num_rounds = 10
        elif key_size == '24':
            num_rounds = 12
        elif key_size == '32':
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
