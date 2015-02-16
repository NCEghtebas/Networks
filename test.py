from constants import *
from translator import *

def decode(message):
    stack = MorseBJStack()
    encoded = stack.decode(message)
    return encoded


def test():
        print("RUNNING TEST CODE")
        

def main():
	test()

if __name__ == "__main__":
	main()
