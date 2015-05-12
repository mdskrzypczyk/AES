#!/usr/bin/python
from sys import argv
from files import key_expansion
import os

script, key, key_size = argv
generated_key = key_expansion.KeyExpansion(key,key_size).expanded_key
