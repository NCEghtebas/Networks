def push_down(ip_protocol, payload, destination):
    from datalinklayer import get_from_ip_layer
    get_from_ip_layer(ip_protocol, payload, destination)

def get_from_datalink_layer(decoded_message):
    protocol = decoded_message["IP_PROTOCOL"]
    payload = decoded_message["PAYLOAD"]
    statement = "=== Using protocol: " + protocol + " ===" + "\n" + "This RaspberryPi received the message: " + payload
    print(statement)

def main():
    destination = input('Recipient (A, B, or C): ')
    payload = input('Input Message: ')
    ip_protocol = "Av0"
    push_down(ip_protocol, payload, destination)

if __name__ == "__main__":
	main()
