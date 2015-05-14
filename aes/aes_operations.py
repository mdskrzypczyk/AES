sbox = open('aes/sbox').read().replace('\n',' ' ).split(' ')
isbox = open('aes/isbox').read().replace('\n',' ').split(' ')
etable = open('aes/etable').read().replace('\n',' ').split(' ')
ltable = open('aes/ltable').read().replace('\n',' ').split(' ')
rcon_box = open('aes/rcon').read().split('\n')


#====================Ascii/Hex string manipulation=====================#
def string_to_hex(in_string):
    #Convert string to list of ascii values
    in_string = [ord(_) for _ in in_string]
    out_hex = ''

    #Convert into a string of hex characters
    for num in in_string:
        if num < 16:
            out_hex += ('0' + hex(num).replace('0x',''))
        else:
            out_hex += hex(num).replace('0x','')

    return out_hex

def hex_to_string(in_hex):
    #Convert hex into a list of ascii values
    in_hex = [int(in_hex[_:_+2],16) for _ in range(0,len(in_hex),2)]

    #Convert into a string of ascii characters
    out_string = ''
    for num in in_hex:
        out_string += chr(num)

    return out_string

def append_length(message):
    #Obtain original length of message
    message_length = len(message)

    #Create a hex representation of it
    hex_length = hex(message_length).replace('0x','')
    while len(hex_length) % 32 != 0:
        hex_length = '0' + hex_length

    return (hex_length + message)



#=============================Key Expansion Functions===========================#
def rot_word(word):
    #Circular shift 1 byte
    return (word[2:]+word[0:2])

def sub_word(word):
    new_word = ''

    #New string contains substituted bytes
    for _ in range(0,len(word),2):
        new_word += sbox[int(word[_],16)*16 + int(word[_+1],16)]

    return new_word

def rcon(val):
    #Return a lookup
    return rcon_box[val]

def ek(expanded_key, offset):
    byte_offset = offset*2
    #Return segment of key
    return expanded_key[byte_offset:byte_offset+8]



#============================Encryption and Decryption Functions=============================#
def add_round_key(current_key, state):
    #Perform XOR on invididual key and state bytes
    new_state = [int(a,16) ^ int(b,16) for a,b in zip(current_key,state)]

    #Turn it back into an ASCII representation
    new_state = ''.join([hex(a).replace('0x','') for a in new_state]).upper()

    return new_state.upper()

def byte_sub(state):
    new_state = ''

    #Perform sbox lookup and return substituted string
    for _ in range(0,len(state),2):
        new_state += sbox[int(state[_],16)*16 + int(state[_+1],16)]

    return new_state

def ibyte_sub(state):
    new_state = ''

    #Perform sbox lookup and return substituted string
    for _ in range(0,len(state),2):
        new_state += isbox[int(state[_],16)*16 + int(state[_+1],16)]

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

def ishift_row(state):
    #Separate state into individual "byte" ascii characters
    new_state = [state[_:_+2] for _ in range(0,len(state),2)]

    #Join every fourth character into it's own 'row' of the state
    first_row = ''.join(new_state[::4])
    second_row = ''.join(new_state[1::4])
    third_row = ''.join(new_state[2::4])
    fourth_row = ''.join(new_state[3::4])

    #Perform the byte shifts on each row
    second_row = second_row[6:] + second_row[0:6]
    third_row = third_row[4:] + third_row[0:4]
    fourth_row = fourth_row[2:] + fourth_row[0:2]

    #Reconstruct a state with the shifted rows
    ret_state = ''
    for _ in range(0,len(state)/2,2):
        ret_state += first_row[_:_+2]
        ret_state += second_row[_:_+2]
        ret_state += third_row[_:_+2]
        ret_state += fourth_row[_:_+2]

    return ret_state

def el(num1,num2):
    if num1 == 0 or num2 == 0:
        return 0
    else:
        new_num = ll(num1)+ll(num2)
    while new_num > 255:
        new_num -= 255
    return int(etable[new_num],16)

def ll(num):
    return int(ltable[num],16)

def mix_column(state):
    #Basic multiplication row, can shift and reuse
    mult = [2,3,1,1]

    #Separate state into individual 'byte' representations and convert to integers
    int_state = [int(state[_:_+2],16) for _ in range(0,len(state),2)]
    
    new_state = []

    #Calculate each row byte using Galois Field
    for _ in range(4):
        bfirst = el(int_state[0],mult[0])^el(int_state[1],mult[1])^el(int_state[2],mult[2])^el(int_state[3],mult[3])
        bsecond = el(int_state[4],mult[0])^el(int_state[5],mult[1])^el(int_state[6],mult[2])^el(int_state[7],mult[3])
        bthird = el(int_state[8],mult[0])^el(int_state[9],mult[1])^el(int_state[10],mult[2])^el(int_state[11],mult[3])
        bfourth = el(int_state[12],mult[0])^el(int_state[13],mult[1])^el(int_state[14],mult[2])^el(int_state[15],mult[3])
        
        #Make sure to remove any leading hex digits
        while bfirst > 255:
            bfirst -= 256
        while bsecond > 255:
            bsecond -= 256
        while bthird > 255:
            bthird -= 256
        while bfourth > 255:
            bfourth -= 256

        #Add onto running list of calculated bytes
        new_state.extend([bfirst,bsecond,bthird,bfourth])

        #Shift multiplication matrix row
        mult = mult[3:] + mult[0:3]

    #Reconstruct in proper order
    new_state = [new_state[_::4] for _ in range(4)]
    new_state = [num for _ in new_state for num in _]

    converted = []

    #Recreate hex representation of each number
    for item in new_state:
        if item < 16:
            converted.append('0'+hex(item).replace('0x',''))
        else:
            converted.append(hex(item).replace('0x',''))

    #Reconstruct hex string
    new_state = ''.join(converted).upper()
    return new_state

def imix_column(state):
    #Basic multiplication row, can shift and reuse
    mult = [14,11,13,9]

    #Separate state into individual 'byte' representations and convert to integers
    int_state = [int(state[_:_+2],16) for _ in range(0,len(state),2)]
    
    new_state = []

    #Calculate each row byte using Galois Field
    for _ in range(4):
        bfirst = el(int_state[0],mult[0])^el(int_state[1],mult[1])^el(int_state[2],mult[2])^el(int_state[3],mult[3])
        bsecond = el(int_state[4],mult[0])^el(int_state[5],mult[1])^el(int_state[6],mult[2])^el(int_state[7],mult[3])
        bthird = el(int_state[8],mult[0])^el(int_state[9],mult[1])^el(int_state[10],mult[2])^el(int_state[11],mult[3])
        bfourth = el(int_state[12],mult[0])^el(int_state[13],mult[1])^el(int_state[14],mult[2])^el(int_state[15],mult[3])
        
        #Make sure to remove any leading hex digits
        while bfirst > 255:
            bfirst -= 256
        while bsecond > 255:
            bsecond -= 256
        while bthird > 255:
            bthird -= 256
        while bfourth > 255:
            bfourth -= 256

        #Add onto running list of calculated bytes
        new_state.extend([bfirst,bsecond,bthird,bfourth])

        #Shift multiplication matrix row
        mult = mult[3:] + mult[0:3]

    #Reconstruct in proper order
    new_state = [new_state[_::4] for _ in range(4)]
    new_state = [num for _ in new_state for num in _]

    converted = []

    #Recreate hex representation of each number
    for item in new_state:
        if item < 16:
            converted.append('0'+hex(item).replace('0x',''))
        else:
            converted.append(hex(item).replace('0x',''))

    #Reconstruct hex string
    new_state = ''.join(converted).upper()
    return new_state