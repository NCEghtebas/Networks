def push_down(message):
    from datalinklayer import get_from_ip_layer
    get_from_ip_layer(message)

def get_from_datalink_layer(decoded_message):
    protocol = decoded_message["IP_PROTOCOL"]
    payload = decoded_message["PAYLOAD"]
    statement = "=== Using protocol: " + protocol + " ===" + "\n" + "This RaspberryPi received the message: " + payload
    print(statement)

def main():
    destination = input('Destination: ')
    while (len(destination) != 2):
        print("ERROR: DESTINATION MUST BE 2 CHARS")
        destination = input('Destination: ')
    payload = input('Input Message: ')
    ip_protocol = "A"

    message = {}
    message["PAYLOAD"] = payload
    message["IP_PROTOCOL"] = ip_protocol
    message["DESTINATION_LAN"] = destination[0]
    message["DESTINATION_HOST"] = destination[1]
    print("MSG: " + str(message))

    push_down(message)

if __name__ == "__main__":
	main()
