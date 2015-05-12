#!/usr/bin/python
from sys import argv
from files import key_expansion
import random

script, key_size = argv
key = ''.join(random.choice('0123456789ABCDEF') for x in range(key_size))
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key
