#!/usr/bin/python
from sys import argv
from aes import key_expansion, decryption, encryption

options, block = argv[1:3]

#If user wants string encrypted
if 's' in options:
	hex_block = string_to_hex(block)
else:
	hex_block = block

#If user wants to provide a key for encryption/decryption
if 'k' in options:
	key = argv[3]
	key_size = len(key)/2
else:
	key_size = int(argv[3])
	key = ''.join(random.choice('0123456789ABCDEF') for x in range(key_size))

#Expand the key
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key

#If user wants to encrypt
if 'e' in options:
	encrypted_message = encryption.Encryption(hex_block, generated_key, key_size).message
	print encrypted_message

#If user wants to decrypt
if 'd' in options:
	decrypted_message = decryption.Decryption(hex_block, generated_key, key_size).message
	print decrypted_message
