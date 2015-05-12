#!/usr/bin/python
from sys import argv
from files import encryption, key_expansion
import random

script, block, key_size = argv
#key = ''.join(random.choice('0123456789ABCDEF') for x in range(key_size))
key = '000102030405060708090A0B0C0D0E0F'
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key
encryption.Encryption(block, generated_key, key_size)
