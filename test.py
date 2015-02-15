from constants import *
from translator import *

def encode(message):
	stack = MorseBJStack()
	encoded = stack.encode(message)
	return encoded

def ip():
	payload = encode(input('Message: '))
	ip = encode("Av0")
	message = datalink(ip, payload)
	print(message)

def datalink(ip, payload):
	dest = encode(input('Recipeint (A B or C)?: '))
	src = encode(mac)
	sep = [(1,1), (1,0), (3,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
	return  [(20,1),(1,0)] + src + sep + dest + sep + ip + sep + payload + [(40,1)]

def main():
	ip()

if __name__ == "__main__":
	main()