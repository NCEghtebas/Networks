import json

def push_down(message):
    from datalinklayer import get_from_ip_layer
    get_from_ip_layer(message)

def get_from_datalink_layer(decoded_message):
    protocol = decoded_message["IP_PROTOCOL"]
    payload = decoded_message["PAYLOAD"]
    statement = "=== Using protocol: " + protocol + " ===" + "\n" + "This RaspberryPi received the message: " + payload
    print(statement)

def main():
    ip = open('ip.txt', 'r+')
    try:
        ip = json.loads(ip)
    except:
        print('Obtain IP.')

        # Request to Router for IP Address
        ip_protocol = "C"
        message = {}
        message["PAYLOAD"] = ' '
        message["IP_PROTOCOL"] = ip_protocol
        message["DESTINATION_LAN"] = "A"
        message["DESTINATION_HOST"] = "1"
        push_down(message)

    ip_protocol = "A"
    destination = input('Destination: ')
    while (len(destination) != 2):
        print("ERROR: DESTINATION MUST BE 2 CHARS")
        destination = input('Destination: ')
    payload = input('Input Message: ')

    message = {}
    message["PAYLOAD"] = payload
    message["IP_PROTOCOL"] = ip_protocol
    message["DESTINATION_LAN"] = destination[0]
    message["DESTINATION_HOST"] = destination[1]
    print("MSG: " + str(message))

    push_down(message)

if __name__ == "__main__":
    main()
