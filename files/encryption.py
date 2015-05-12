sbox = open('files/sbox').read().replace('\n',' ' ).split(' ')

def add_round_key(current_key, state):
    new_state = ''.join([int(a,16) ^ int(b,16) for a,b in zip(current_key,state)])
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
    



class Encryption:
    def __init__(self, block, key, key_size):
        self.message_length = len(block)
        self.message = ''
        while len(block) % 32 != 0:
            block += '0'
        
        if key_size == '16':
            num_rounds = 9
        elif key_size == '24':
            num_rounds = 11
        elif key_size == '32':
            num_rounds = 13

        block_start = 0
        for encryptions in range(len(block)/32):
            add_round_key(key[0:32], block[block_start:block_start+32])

            for encryption_round in range(num_rounds):
                mix_column(add_round_key(key[encryption_round*32:(encryption_round+1)*32], byte_sub(shift_row(block[block_start:block_start+32]))))

            add_round_key(key[num_rounds*32:(num_rounds+1)*32], byte_sub(shift_row(block[block_start:block_start+32])))
            block_start += 32























