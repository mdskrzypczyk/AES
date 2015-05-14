# AES
Python AES encryption program

Algorithm for encryption obtained from the following documentation: http://www.adamberent.com/documents/aesbyexample.pdf

## Dependencies
This package requires Python 2.7

## Usage

./run.py -[options] [message]...(key) (key size)

## Inputs
options: The following options are provided in this distribution.
-e      Encrypt - This signals the script to encrypt the provided message
-d      Decrypt - This signals the script to decrypt the provided message
-k      Use Key - This signals the script to use the user provided key
-s      String - The encryption input is a string or the decryption output will
                 be a string

message: This is the message that the script is to encrypt or decrypt.

key: If 'k' is provided within the options then this is the key provided by the
     user.  The key must be provided in hex and must have byte length of 16, 24,
     or 32

key size: If 'k' is not provided then the user must specify the use of a 16, 24,
          or 32 byte long key.

## Outputs
The encrypted or decrypted message is output onto the screen.  If the user specifies the 'k' option then the key used for encryption will be provided to the user.
