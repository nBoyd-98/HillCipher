import numpy
from numpy.linalg import inv
from numpy.linalg import det
import sympy
from sympy import mod_inverse
import sys


def main():

	#Input validation
	argc = len(sys.argv) - 1
	if argc != 1:
		print("Improper number of arguments")
		quit()
	elif (not sys.argv[1] == "-e") and (not sys.argv[1] == "-d"):
		print("Only '-e' and '-d' arguments accepted")
		quit()

	msg = input("Please enter message: ").upper()
	key = input("Please enter key: ").upper()

	if charcount(key) > 9:
		print("Key value may only have at most 9 characters")
		quit()

	msg_list = to_int_list(msg)
	key_list = to_int_list(key)

	n = get_n(key_list)
	key_matrix = create_key_matrix(key_list, n)

	if not has_inverse(key_matrix):
		print("Provided key has no inverse and is not a valid!")
		quit()

	msg_list = fix_int_list(msg_list, n)
	msg_matrix = numpy.array(msg_list)

	msg_matrix = fix_msg_matrix(msg_matrix, n)

	if sys.argv[1] == '-e':
		encrypt(msg_matrix, key_matrix)
		quit()
	elif sys.argv[1] == '-d':
		decrypt(msg_matrix, key_matrix, n)
		quit()
	else:
		print("Only '-e' and '-d' arguments accepted")
		quit()





def to_int_list(string):
	l = []
	for c in string:
		if not (ord(c) == 32):
			n = (ord(c) - 65) % 26
			l.append(n)
	return l

def fix_int_list(msg_list, n):
	while not (len(msg_list)%n == 0):
		msg_list.append(25)

	return msg_list

def fix_msg_matrix(msg_matrix, n):
	c = len(msg_matrix) / n
	new = numpy.split(msg_matrix, c)  
	return new

def encrypt(msg, key):
	elist = []
	for group in msg:
		e = numpy.dot(key, group)%26
		elist.append(e)

	string = []
	for array in elist:
		for element in array:
			string.append(chr(int(element)+65))

	message = ''.join(string)
	print("Encrypted message: " + message)

def decrypt(msg, key, n):
	dec_key = get_inverse(key, n)
	dlist = []
	for group in msg:
		d = numpy.dot(dec_key, group)%26
		dlist.append(d)

	string = []
	for array in dlist:
		for element in array:
			string.append(chr(int(element)+65))

	message = ''.join(string)
	print("Decrypted message: " + message)

def charcount(string):
	count = 0
	for c in string:
		if not(ord(c) == 32):
			count += 1

	return count

def get_n(key_list):
	length = len(key_list)
	if length <= 4:
		n = 2
		return n
	elif 4 < length <= 9:
		n = 3
		return n
	else:
		print("Key length error!!")



def create_key_matrix(key_list, n):
	key_matrix = numpy.zeros(shape=(n, n))
	for (i, j) in zip(range(0, len(key_list)), key_list):
		a, b = i/n, i%n
		key_matrix[int(a), int(b)] = j

	return key_matrix


def has_inverse(key_matrix):
	det = int(round((numpy.linalg.det(key_matrix)%26)))
	print("det: " + str(det))
	if det == 0:
		print("1")
		return False
	else:
		try:
			tmp = sympy.mod_inverse(det, 26)
		except:
			print("333")
			return False

	return True

def get_inverse(key_matrix, n):
	inv_det = sympy.mod_inverse((int(round(numpy.linalg.det(key_matrix)%26))), 26)


	if n == 2:
		adj = numpy.zeros(shape=(n, n))
		adj[0][0] = key_matrix[1][1]
		adj[1][1] = key_matrix[0][0]
		adj[0][1] = (key_matrix[0][1])*-1
		adj[1][0] = (key_matrix[1][0])*-1
		inv_key_matrix = numpy.dot(inv_det, adj)
		return inv_key_matrix

	else:
		adj = numpy.zeros(shape=(n, n))
		flip = True
		for row in range(3):
			for col in range(3):
				tmp  = numpy.delete(key_matrix, row, axis=0)
				tmp = numpy.delete(tmp, col, axis=1)
				det = int(round(numpy.linalg.det(tmp)))%26
				if not flip:
					det = (det*-1)%26
				adj[col][row] = det
				flip = not flip

		inv_key_matrix = numpy.dot(inv_det, adj)%26
		return inv_key_matrix

main()
