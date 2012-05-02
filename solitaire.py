
import argparse

class Suit:
	def __init__(self, name, starting_value):
		self.name = name
		self.val = starting_value

	def __eq__(self, other):
		return self.val == other.val and self.name == other.name

	def get_value(self, card_value):
		return self.val + card_value

clubs = Suit("clubs", 0)
diamonds = Suit("diamonds", 13)
hearts = Suit("hearts", 26)
spades = Suit("spades", 39)
jokers = Suit("jokers", 52)

class Card:
	def __init__(self, suit, name, val):
		self.suit = suit
		self.val = val
		self.name = name

	def __eq__(self, other):
		return self.suit == other.suit and self.name == other.name and self.val == other.val

	def __str__(self):
		return "%s of %s" % (self.name, self.suit.name)

	def get_value(self):
		return self.suit.get_value(self.val)

	def get_full_name(self):
			return "%s of %s (%s)" % (self.name, self.suit.name, self.get_value())


A_joker = Card(jokers, "A", 1)
B_joker = Card(jokers, "B", 1)			

def create_sorted_deck():
	def create_suit_of_cards(suit):
		result = []
		result.append(Card(suit, "ace", 1))
		for i in range(2, 11):
			result.append(Card(suit, str(i), i))
		result.append(Card(suit, "jack", 11))
		result.append(Card(suit, "queen", 12))
		result.append(Card(suit, "king", 13))
		return result

	result = []
	for s in [clubs, diamonds, hearts, spades]:
		for c in create_suit_of_cards(s):
			result.append(c)
	result.append(Card(jokers, "A", 1))
	result.append(Card(jokers, "B", 1))
	return result

def move_A(deck):
	l = len(deck)
	i = deck.index(A_joker)
	if i == len(deck) - 1: # last card
		return [A_joker] + deck[:l-1]
	else:
		return deck[:i] + [deck[i+1]] + [A_joker] + deck[i+2:]

def move_B(deck):
	l = len(deck)
	i = deck.index(B_joker)
	if i == len(deck) - 1: # last card
		return deck[:2] + [B_joker] + deck[2:l-1]
	elif i == len(deck) - 2: # second to last
		return [deck[0]] + [B_joker] + deck[1:l-2] + [deck[l-1]]
	else:
		return deck[:i] + deck[i+1:i+3] + [B_joker] + deck[i+3:]

def triple_cut(deck):
	ii = sorted([deck.index(A_joker), deck.index(B_joker)])
	return deck[ii[1]+1:] + deck[ii[0]:ii[1]+1] + deck[:ii[0]]

def count_cut(deck, count):
	return deck[count:] + deck[:count]

def get_output(deck):
	return deck[deck[0].get_value()].get_value()

step1 = move_A
step2 = move_B
step3 = triple_cut
step4 = lambda d: count_cut(d[:len(d)-1], d[len(d)-1].get_value()) + [d[len(d)-1]]

def create_key_stream(deck):
	d = deck
	while True:
		d = step4(step3(step2(step1(d))))
		o = get_output(d)
		if o != 53:
			yield o

# ------



CHAR_TO_NUMBER_MAP = {
	'A':1,  'B':2,  'C':3,  'D':4,  'E':5,
	'F':6,  'G':7,  'H':8,  'I':9,  'J':10,
	'K':11, 'L':12, 'M':13, 'N':14, 'O':15,
	'P':16, 'Q':17, 'R':18, 'S':19, 'T':20,
	'U':21, 'V':22, 'W':23, 'X':24, 'Y':25,
	'Z':26
}

def char_to_nr(c):
	return CHAR_TO_NUMBER_MAP[c.upper()]

def strip_bad_chars(str):
	for c in str:
		if c.isalpha():
			yield c

def invert_dict(x):
	result = dict()
	for k in x.keys():
		result[x[k]] = k
	return result

NUMBER_TO_CHAR_MAP = invert_dict(CHAR_TO_NUMBER_MAP)

def nr_to_char(nr):
	return NUMBER_TO_CHAR_MAP[nr]

def encrypt(plain, deck):
	stripped = "".join(strip_bad_chars(plain))
	extra = ""
	if len(stripped) % 5 > 0:
		for x in range(-1 * ((len(stripped) % 5) - 5)):
			extra = extra + "X"

	str_stream = map(char_to_nr, stripped + extra)
	encrypted_stream = map(lambda x, y: ((x + y - 1) % 26) + 1, str_stream, create_key_stream(deck))
	return "".join(nr_to_char(x) for x in encrypted_stream)

def decrypt(cypher, deck):
	str_stream = map(char_to_nr, strip_bad_chars(cypher))
	plain_stream = map(lambda x, y: ((x - y - 1) % 26) + 1, str_stream, create_key_stream(deck))
	return "".join(nr_to_char(x) for x in plain_stream)

# ------ 

def repeat_stream(stream, times):
	for i in range(times):
		for j in stream:
			yield j

def take(stream, count):
	for i in range(count):
		yield next(stream)

def pretty_print(txt):
	if len(txt) == 0:
		return ""
	return txt[:5] + " " + pretty_print(txt[5:])

def create_key_based_deck(key, repeats):
	d = create_sorted_deck()
	key_str_stream = map(char_to_nr, key)
	for cut in repeat_stream(key_str_stream, repeats):
		d = step4(step3(step2(step1(d))))
		d = count_cut(d[:len(d)-1], cut) + [d[len(d)-1]]
	return d

# ------

parser = argparse.ArgumentParser(description='Encrypts and decrypts plain text using the Solitaire algorithm made famous by the book Cryptonomicon by Neal Stephonson and invented by Bruce Schneier')
parser.add_argument('key', type=str, help='the passphrase with which the text is encrypted. Remember never to use the same passphrase twice!')
parser.add_argument('times', type=int, default=1, help='the number of times the passphrase will be repeated to create a longer passphrase')
parser.add_argument('mode', type=str, choices=['enc', 'dec'], help='the mode of the operation. enc for encryption and dec for decrypting')
parser.add_argument('message', type=str, nargs='+', help='the message that must be sent')
env = parser.parse_args()

key = create_key_based_deck(env.key, env.times)

if env.mode == 'enc':
	print(pretty_print(encrypt(" ".join(env.message), key)))
else:
	print(pretty_print(decrypt(" ".join(env.message), key)))

