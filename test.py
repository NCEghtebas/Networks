from constants import *
from translator import *
#
# def encode(message):
#	 stack = MorseBJStack()
#	 encoded = stack.encode(message)
#	 return encoded
#
# def ip():
#	 payload = encode(input('Message: '))
#	 ip = encode("Av0")
#	 message = datalink(ip, payload)
#	 print(message)
#
# def datalink(ip, payload):
#	 dest = encode(input('Recipeint (A B or C)?: '))
#	 src = encode(mac)
#	 sep = [(1,1), (1,0), (3,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
#	 return  [(20,1),(1,0)] + src + sep + dest + sep + ip + sep + payload + [(40,1)]

def find_end(pulses):
	end_header = [(3,1), (1,0), (1,1), (1,0), (1,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
	for i in range(len(pulses)):
		if pulses[i] == end_header[0]:
			for j in range(len(end_header)):
				if pulses[i+j] != end_header[j]:
					break
				else:
					print("i " + str(i))
					print("j " + str(j))
					if j == len(end_header)-1:
						return i+j

def bonnie(pulse):
    str_pulse = str(pulse)
    print(str_pulse)
    end_header = "(3, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (3, 1), (1, 0)"
    print(end_header)
    index = str_pulse.find(end_header)
    msg = str_pulse.split(end_header)
    header = str_pulse[0]
    print("MESSAGE: " + str(msg))

def test():
        pulse = [(20, 1), (1, 0), (1, 1), (1, 0), (3, 1), (3, 0), (1, 1), (1, 0), (3, 1), (1, 0), (1, 1), (1, 0), (3, 1), (1, 0), (1, 1), (1, 0), (3, 1), (3, 0), (1, 1), (1, 0), (3, 1), (1, 0), (1, 1), (1, 0), (3, 1), (1, 0), (1, 1), (1, 0), (3, 1), (3, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (3, 1), (3, 0), (3, 1), (1, 0), (3, 1), (1, 0), (3, 1), (1, 0), (3, 1), (1, 0), (3, 1), (3, 0), (3, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (3, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (1, 0), (1, 1), (3, 0), (1, 1), (3, 0), (1, 1), (1, 0), (3, 1), (1, 0), (1, 1), (1, 0), (1, 1), (3, 0), (1, 1), (1, 0), (3, 1), (1, 0), (1, 1), (1, 0), (1, 1), (3, 0), (3, 1), (1, 0), (3, 1), (1, 0), (3, 1), (3, 0), (40, 1)]
        p = bonnie(pulse)
        print(p)

def main():
	test()

if __name__ == "__main__":
	main()
##from constants import *
##from translator import *

##def encode(message):
##	stack = MorseBJStack()
##	encoded = stack.encode(message)
##	return encoded
##
##def ip():
##	payload = encode(input('Message: '))
##	ip = encode("Av0")
##	message = datalink(ip, payload)
##	print(message)
##
##def datalink(ip, payload):
##	dest = encode(input('Recipeint (A B or C)?: '))
##	src = encode(mac)
##	sep = [(1,1), (1,0), (3,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
##	return  [(20,1),(1,0)] + src + sep + dest + sep + ip + sep + payload + [(40,1)]
##
##def main():
##	ip()
##
##if __name__ == "__main__":
##	main()
