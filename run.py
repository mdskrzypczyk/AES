#!/usr/bin/python
from sys import argv
from files import encryption, key_expansion
import random

script, block, key_size = argv

#This is for generating a random key
#key = ''.join(random.choice('0123456789ABCDEF') for x in range(key_size))
key = '000102030405060708090A0B0C0D0E0F'

#Expand the key
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key

#Encrypt the message
encrypted_message = encryption.Encryption(block, generated_key, key_size).message
print encrypted_message
