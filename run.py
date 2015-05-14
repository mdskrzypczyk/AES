#!/usr/bin/python
from sys import argv, exit
from aes import key_expansion, decryption, encryption, aes_operations
import random

#Check if arguments supplied
if len(argv) == 0:
	print 'Script use: ./run.py -[options] [block]'
	exit()

#Check options
options = argv[1]

if '-' not in options:
	print 'Invalid options'
	print 'Script use: ./run.py -[options] [block]'
	print '=========Options========='
	print '-k       Use user provided key'
	print '-s       Input block is string'
	print '-e       Encrypt message'
	print '-d       Decrypt message'
	print 'Please include all options together (i.e. -ske)'
	exit()

#Check message block
if len(argv) < 3:
	print 'No message block provided'
	exit()

block = argv[2]
#If user wants string encrypted
if 's' in options:
	hex_block = aes_operations.string_to_hex(block)
else:
	hex_block = block

#If user wants to provide a key for encryption/decryption
if 'k' in options:
	if len(argv) < 4:
		print 'No key provided'
		exit()
	key = argv[3]
	key_size = len(key)/2
else:
	if len(argv) < 4:
		print 'No key size provided'
		exit()
	key_size = int(argv[3])
	key = ''.join(random.choice('0123456789ABCDEF') for x in range(key_size))

#Expand the key
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key

#If user wants to encrypt
if 'e' in options:
	encrypted_message = encryption.Encryption(hex_block, generated_key, key_size).message
	print 'Encrypted message: ' + encrypted_message
	exit()

#If user wants to decrypt
if 'd' in options:
	decrypted_message = decryption.Decryption(hex_block, generated_key, key_size).message
	print 'Decrypted message: ' + decrypted_message
	exit()
