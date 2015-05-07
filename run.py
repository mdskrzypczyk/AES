#!/usr/bin/python
from sys import argv

script, operation, block, key_size = argv

if operation == 'encrypt':
    pass
elif operation == 'decrypt':
    pass
else:
    print 'This program is designed to be used in the following:'
    print 'run.py [operation] [block] [key_size]'
    print 'operation: encrypt or decrypt'
    print 'block: block to perform operation on'
    print 'key_size: the key size to use'
