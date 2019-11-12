# HillCipher
Implementation of the hill cipher in python using numpy and sympy. Takes at most a 3x3 (9 character) matrix key. Quite hacky and slow but gets the job done.

# Usage
hill.py [-e | -d]

-e: Encryption mode, prompts for message and key, creates cipher text.

-d: Decryption mode, prompts for cipher text and key, calculates inverse mod of key, creates original message.

Valid input is limited to alphabetical characters only. 

