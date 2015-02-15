from datalinklayer import get

def push(ip_protocol, payload, destination):
    get(ip_protocol, payload, destination)

def main():
    destination = input('Recipient (A, B, or C): ')
    payload = input('Input Message: ')
    ip_protocol = "Av0"
    push(ip_protocol, payload, destination)

if __name__ == "__main__":
	main()
