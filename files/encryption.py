sbox = open('files/sbox').read().replace('\n',' ' ).split(' ')

def add_round_key(current_key, state):
    new_state = [int(a,16) ^ int(b,16) for a,b in zip(current_key,state)]
    new_state = ''.join([hex(a).replace('0x','') for a in new_state]).upper()
    return new_state

def byte_sub(state):
    new_state = ''
    for _ in range(0,len(state),2):
        new_state += sbox[int(state[_],16)*16 + int(state[_+1],16)]

    return new_state

def shift_row(state):
    new_state = [state[_:_+2] for _ in range(0,len(state),2)]
    first_row = ''.join(new_state[::4])
    second_row = ''.join(new_state[1::4])
    third_row = ''.join(new_state[2::4])
    fourth_row = ''.join(new_state[3::4])
    second_row = second_row[2:] + second_row[0:2]
    third_row = third_row[4:] + third_row[0:4]
    fourth_row = fourth_row[6:] + fourth_row[0:6]
    ret_state = ''
    for _ in range(0,len(state)/2,2):
        ret_state += first_row[_:_+2]
        ret_state += second_row[_:_+2]
        ret_state += third_row[_:_+2]
        ret_state += fourth_row[_:_+2]
    return ret_state

def mix_column(state):
    mult_row = [2,3,1,1]
    int_state = [state[_:_+2] for _ in range(0,len(state),2)]
    print int_state
    int_state = [int(a,16) for a in int_state]
    print int_state
    new_state = []
    for _ in range(4):
        print mult_row
        bfirst = (int_state[0] * mult_row[0]) ^ (int_state[1] * mult_row[1]) ^ (int_state[2] * mult_row[2]) ^ (int_state[3] * mult_row[3])
        bsecond = (int_state[4] * mult_row[0]) ^ (int_state[5] * mult_row[1]) ^ (int_state[6] * mult_row[2]) ^ (int_state[7] * mult_row[3])
        bthird = (int_state[8] * mult_row[0]) ^ (int_state[9] * mult_row[1]) ^ (int_state[10] * mult_row[2]) ^ (int_state[11] * mult_row[3])
        bfourth = (int_state[12] * mult_row[0]) ^ (int_state[13] * mult_row[1]) ^ (int_state[14] * mult_row[2]) ^ (int_state[15] * mult_row[3])
        new_state.extend([bfirst, bsecond, bthird, bfourth])
        print new_state
        mult_row = mult_row[3:] + mult_row[0:3]

    new_state = [new_state[_::4] for _ in range(4)]
    print new_state
    new_state = [num for _ in new_state for num in _]
    print new_state
    new_state = ''.join([hex(a).replace('0x','') for a in new_state]).upper()
    return new_state

class Encryption:
    def __init__(self, block, key, key_size):
        self.message_length = len(block)
        self.message = ''
        while len(block) % 32 != 0:
            block += '0'
        
        print mix_column(shift_row(byte_sub(add_round_key(key[0:32],block[0:32]))))

        if key_size == '16':
            num_rounds = 9
        elif key_size == '24':
            num_rounds = 11
        elif key_size == '32':
            num_rounds = 13

        #block_start = 0
        #for encryptions in range(len(block)/32):
        #    add_round_key(key[0:32], block[block_start:block_start+32])

        #    for encryption_round in range(num_rounds):
        #        mix_column(add_round_key(key[encryption_round*32:(encryption_round+1)*32], byte_sub(shift_row(block[block_start:block_start+32]))))

        #    add_round_key(key[num_rounds*32:(num_rounds+1)*32], byte_sub(shift_row(block[block_start:block_start+32])))
        #    block_start += 32























