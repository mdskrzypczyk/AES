sbox = open('sbox').read().replace('\n',' ').split(' ')
rcon_box = open('rcon').read().replace('\n', '').split()
def rot_word(word):
    return (word[2:]+word[0:1])

def sub_word(word):
    for _ in range(len(word)/2):
        word.replace(word[_:_+2], sbox[int(word[_],16)*16 + int(word[_+1])])

    return word

def rcon(val):


def ek():

def k():

KeyExpansion:
    def __init__(self, key, key_size):
        self.expanded_key
