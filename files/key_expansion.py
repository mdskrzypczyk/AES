sbox = open('files/sbox').read().replace('\n',' ').split(' ')
rcon_box = open('files/rcon').read().split('\n')

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

class KeyExpansion:
    def __init__(self, key, key_size):
        self.expanded_key = ''
        self.expanded_key += key

        #Expand key differently based on request
        if key_size == '16':
            start_round = 4
            rounds = 44
            sig_round = 4
        elif key_size == '24':
            start_round = 6
            rounds = 52
            sig_round = 6
        elif key_size == '32':
            start_round = 8
            rounds = 60
            sig_round = 8

        #Iterate over the number of rounds
        for expansion_round in range(start_round, rounds):
            #If round is a multiple of number of rounds for specified key size
            if (expansion_round % sig_round) == 0:
                first_ek = ek(self.expanded_key, (expansion_round-1)*4)
                first_ek = sub_word(rot_word(first_ek))
                r_con = rcon((expansion_round/sig_round)-1)
                second_ek = ek(self.expanded_key, (expansion_round-sig_round)*4)
                arg = [int(a,16) ^ int(b,16) ^ int(c,16) for a,b,c in zip(first_ek,r_con,second_ek)]

            else:
                first_ek = ek(self.expanded_key, (expansion_round-1)*4)
                second_ek = ek(self.expanded_key, (expansion_round-sig_round)*4)
                arg = [int(a,16) ^ int(b,16) for a,b in zip(first_ek,second_ek)]

            arg = ''.join([hex(a).replace('0x','') for a in arg]).upper()
            self.expanded_key += arg
