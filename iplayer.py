from datalinklayer import get_from_ip_layer

def push_down(ip_protocol, payload, destination):
    get_from_ip_layer(ip_protocol, payload, destination)

def main():
    destination = input('Recipient (A, B, or C): ')
    payload = input('Input Message: ')
    ip_protocol = "Av0"
    push_down(ip_protocol, payload, destination)

if __name__ == "__main__":
	main()
