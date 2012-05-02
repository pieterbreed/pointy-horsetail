Solitaire in python
===================

"Pointy horsetail" is an anagram of "python solitaire"

This is an implementation of the [solitaire encryption algorithm which was invented by Bruce Schneier] [1]. 

  [1]: http://www.schneier.com/solitaire.html

The algorithm featured prominently in a book called [Cryptonomicon written by Neal Stephenson] [2].

  [2]: http://en.wikipedia.org/wiki/Cryptonomicon

Code Status
===========

The code was banged out in day of me trying to learn python, so I'm sure it's not pythonistic, but it works, more-or-less.

I tested it on Windows 7 64, using python 3.2

Examples
========

Use the python app like this to encrypt a message:

    > python solitaire.py secretkey 3 enc this is a secret message

produces: `FZVXQ BWFBQ LNDMG WBSRM`

The other party must use the following invocation to decrypt the message:

    > python solitaire.py secretkey 3 dec FZVXQ BWFBQ LNDMG WBSRM   

produces: `THISI SASEC RETME SSAGE`

The parameters mean:

 - secretkey: This is one half of the secret exchanged between parties A and B trying to communicate securely. This is the 'password' that 'locks' the message. The initial sorted
   deck of cards is permuted based on the solitaire algorithm using the numerical values of the characters in the key. Steps 1 - 4 are performed as normal, with an aditional 'count-cut' step
   performed with a count equal to the numerical value of the each succesive key character. 
 - 3: This is the other half of the secret. The meaning of this is that the initial, sorted deck of cards is permuted so many times in order, ie, the key permutation is performed as if the 
   key's characters were repeated this many times.
 - enc: this is the mode, 'enc' for encryption and 'dec' for decryption
 - everything else: This is the message that is exchanged by the parties. any funny characters are stripped (including spaces). 'X' characters are padded at the end to have a number of plaintext
   characters that are a round power of 5 (5, 10, 25 etc)




