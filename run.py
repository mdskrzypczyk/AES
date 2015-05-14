#!/usr/bin/python
from sys import argv
from aes import key_expansion, decryption, encryption

script, block, key_size = argv

#This is for generating a random key
#key = ''.join(random.choice('0123456789ABCDEF') for x in range(key_size))

block = [ord(_) for _ in block]
print block
hex_block = ''
for num in block:
	if num < 16:
		hex_block += ('0' + hex(num).replace('0x',''))
	else:
		hex_block += hex(num).replace('0x','')

key = '000102030405060708090A0B0C0D0E0F'

#hex_block = block

#Expand the key
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key

#Encrypt the message
encrypted_message = encryption.Encryption(hex_block, generated_key, key_size).message
print encrypted_message

decrypted_message = decryption.Decryption(encrypted_message, generated_key, key_size).message
print decrypted_message