#!/usr/bin/python
from sys import argv, exit
from aes import key_expansion, decryption, encryption, aes_operations
import random
import string

print
#Check if arguments supplied
if len(argv) == 1:
	print 'Script use: ./run.py -[options] [block]'
	print 'If message contains spaces, provide the message in double quotes'
	print 'If quotations made within message place them between single quotes'
	exit()

#Check options
options = argv[1]
if '-' not in options:
	print 'Invalid options'
	print 'Script use: ./run.py -[options] [block]'
	print '=========Options========='
	print '-k       Use user provided key'
	print '         Note: if providing key, add onto end of argument list'
	print '-s       Input block is string'
	print '-e       Encrypt message'
	print '-d       Decrypt message'
	print '-f       Use file'
	print 'Please include all options together (i.e. -ske)'
	exit()

#Check message block
if len(argv) < 3:
	print 'No message block provided'
	exit()

block = argv[2]

if 'f' in options:
	block = open(block).read()
	

#If user wants string encrypted
if 's' in options:
	hex_block = aes_operations.string_to_hex(block)
else:
	#If user chooses to encrypt hex must check if characters are hex
	if all(chars in string.hexdigits for chars in block) is not True:
		print 'Provided hex-string is not all hex'
		exit()
	hex_block = block

#If user wants to provide a key for encryption/decryption
key_sizes = [16,24,32]
if 'k' in options:
	if len(argv) < 4:
		print 'No key provided'
		exit()

	key = argv[3]
	key_size = len(key)/2
	if key_size not in key_sizes:
		print 'Invalid key size, key must be 16, 24, or 32 bytes'
		exit()
else:
	if len(argv) < 4:
		print 'No key size provided'
		exit()

	if all(chars in string.digits for chars in argv[3]) is not True:
		print 'Invalid key size, must be 16, 24, or 32 bytes'
		exit()

	key_size = int(argv[3])

	#Check if key size requested is valid
	if key_size not in key_sizes:
		print 'Invalid key size, must be 16, 24, or 32 bytes'
		exit()

	key = ''.join(random.choice('0123456789ABCDEF') for x in range(key_size*2))

#Expand the key
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key

#If user wants to encrypt
if 'e' in options:
	encrypted_message = encryption.Encryption(hex_block, generated_key, key_size).message
	print 'Encrypted message: ' + encrypted_message
	if 'k' not in options:
		print 'Key used: ' + key
	exit()

#If user wants to decrypt
elif 'd' in options:
	if all(chars in string.hexdigits for chars in block) is not True or (len(block) % 32 != 0):
		print 'Decryption must take hex string as input, string data must be multiple of 16 bytes'
		exit()

	decrypted_message = decryption.Decryption(block, generated_key, key_size).message
	if 's' in options:
		decrypted_message = aes_operations.hex_to_string(decrypted_message)
	print 'Decrypted message: ' + decrypted_message
	if 'k' not in options:
		print 'Key used: ' + key
	exit()

else:
	print 'Encryption/decryption not specfied'
	exit()
