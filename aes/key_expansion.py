from aes_operations import *

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
