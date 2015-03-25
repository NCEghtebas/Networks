from translator import *
from constants import *
import json

def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll-1))

    return results

def encode(message):
    stack = MorseBJStack()
    encoded = stack.encode(message)
    return encoded

def decode(message):
    stack = MorseBJStack()
    encoded = stack.decode(message)
    return encoded

def encode_message_dict(message):
    message['SOURCE_MAC'] = encode(mac_address)
    message['DESTINATION_MAC'] = encode('R') #hard-coded router mac
    message['SOURCE_LAN'] = encode(src_lan)
    message['SOURCE_HOST'] = encode(src_host)
    message["DESTINATION_LAN"] = encode(message["DESTINATION_LAN"])
    message["DESTINATION_HOST"] = encode(message["DESTINATION_HOST"])
    message["IP_PROTOCOL"] = encode(message["IP_PROTOCOL"])
    message['CHECKSUM'] = encode("C") #replace with checksum function
    message["PAYLOAD"] = encode(message["PAYLOAD"])

    sep = [(7,1), (1,0)]
    end_header = [(3,1), (1,0), (1,1), (1,0), (1,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    start = [(20,1),(1,0)]
    stop = [(40,1)]

    return start + message['SOURCE_MAC'] + sep + message['DESTINATION_MAC'] + sep + message['SOURCE_LAN'] + sep + message['SOURCE_HOST'] + sep + message["DESTINATION_LAN"] + sep + message["DESTINATION_HOST"] + sep + message["IP_PROTOCOL"] + sep + message['CHECKSUM'] + end_header + message["PAYLOAD"] + stop


def decode_header(header, end_header_index):
    sep = [(7,1), (1,0)]
    sep_indices = find_sub_list(sep,header)
    header_items = []
    last = 0
    for f in sep_indices:
        item = header[last:f[0]]
        header_items.append(item)
        last = f[1]+1
    protocol = header[last:end_header_index-1]
    header_items.append(protocol)
    decoded_header = {}
    count = 0
    for item in header_items:
        d = decode(item)
        print(d)
        if count == 0:
            decoded_header["SOURCE_MAC"] = d
        elif count == 1:
            decoded_header["DESTINATION_MAC"] = d
        elif count == 2:
            decoded_header["SOURCE_LAN"] = d
        elif count == 3:
            decoded_header["SOURCE_HOST"] = d
        elif count == 4:
            decoded_header["DESTINATION_LAN"] = d
        elif count == 5:
            decoded_header["DESTINATION_HOST"] = d
        elif count == 6:
            decoded_header["IP_PROTOCOL"] = d
        elif count == 7:
            decoded_header["CHECKSUM"] = d
        elif count == 8:
            decoded_header["PAYLOAD"] = d
        count += 1
    return decoded_header

def decode_message(message):
    #Declare End Header Sequence
    end_header = [(3,1), (1,0), (1,1), (1,0), (1,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    end_header_indices = find_sub_list(end_header,message)
    print(end_header_indices)
    end_header_indices = end_header_indices[0]

    #Split message according to header and payload
    header = message[1:end_header_indices[1]+1]
    payload = message[end_header_indices[1]+1:len(message)-1]

    #decode header
    decoded_message = decode_header(header, end_header_indices[0])

    #check if packet is for me or someone else
    #if for someone else, do nothing or reroute packet
    print("DECODED: " + str(decoded_message))

    if (decoded_message['DESTINATION_MAC'] != mac):
        return decoded_message['DESTINATION_MAC']

    #Remove Source & Destination information from message
    decoded_message.pop("SOURCE_MAC", None)
    decoded_message.pop("DESTINATION_MAC", None)
    decoded_message.pop("SOURCE_LAN", None)
    decoded_message.pop("SOURCE_HOST", None)
    decoded_message.pop("DESTINATION_LAN", None)
    decoded_message.pop("DESTINATION_HOST", None)
    decoded_message.pop("CHECKSUM", None)

    #decode payload
    decoded_message["PAYLOAD"] = decode(payload)

    return decoded_message

def push_up(decoded_message):
    from iplayer import get_from_datalink_layer
    get_from_datalink_layer(decoded_message)

def push_down(encoded_message):
    from transmit import get_from_datalink_layer
    get_from_datalink_layer(encoded_message)

def get_from_ip_layer(message):
    #encode the entire message
    mac_address = mac
    src_lan = "A"
    #src_host = "1" #should actually be pulled from router

    if message['IP_PROTOCOL'] == 'C':
        src_host = ' '
    else:
        ip = json.loads(open('ip.txt', 'r+'))
        src_host = ip['IP']

    message['SOURCE_MAC'] = encode(mac_address)
    message['DESTINATION_MAC'] = encode('R') #hard-coded router mac
    message['SOURCE_LAN'] = encode(src_lan)
    message['SOURCE_HOST'] = encode(src_host)
    message["DESTINATION_LAN"] = encode(message["DESTINATION_LAN"])
    message["DESTINATION_HOST"] = encode(message["DESTINATION_HOST"])
    message["IP_PROTOCOL"] = encode(message["IP_PROTOCOL"])
    message['CHECKSUM'] = encode("C") #replace with checksum function
    message["PAYLOAD"] = encode(message["PAYLOAD"])

    #start|stop code for msg and header
    sep = [(7,1), (1,0)]
    end_header = [(3,1), (1,0), (1,1), (1,0), (1,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    start = [(20,1),(1,0)]
    stop = [(40,1)]

    push_down(start + message['SOURCE_MAC'] + sep + message['DESTINATION_MAC'] + sep + message['SOURCE_LAN'] + sep + message['SOURCE_HOST'] + sep + message["DESTINATION_LAN"] + sep + message["DESTINATION_HOST"] + sep + message["IP_PROTOCOL"] + sep + message['CHECKSUM'] + end_header + message["PAYLOAD"] + stop)


def get_from_physical_layer(message):
    #print("PULSES: " + str(message))

    # Check if MAC is mine
    decoded = decode_message(message)
    decoded_len = len(decoded)
    mac_address_len = 1
    if decoded_len == mac_address_len:
        print("REROUTE MESSAGE TO IP ADDRESS: " + decoded)
    else:
        if decoded['DESTINATION_MAC'] == 'R': #this Pi is a Router
          if decoded['IP_PROTOCOL'] == 'C' and decoded['SOURCE_HOST'] == '': #this is an IP Message
            #Pi is requesting for an IP, let's give him one
            ip_tables = open('ip_tables.txt', 'r+')
            ip = open('ip.txt', 'r+')

            try:
                json.loads(ip_tables)
                print('Something in IP Tables')
            except:
                #insert router IP first
                router_ip = {'1': 'R'}
                print('Dumping Router IP: ', router_ip)
                json.dump(router_ip, ip_tables)
                json.dump({'IP': 1}, ip)

            ip_tables = open('ip_tables.txt', 'r+')
            ips = json.loads(ip_tables)
            ip_count = len(ips)
            assigned_ip = ip_count + 1
            ips[str(assigned_ip)] = decoded['SOURCE_MAC']
            json.dump(ips, ip_tables)

            #send packet back to Pi
            decoded['DESTINATION_HOST'] = assigned_ip
            decoded['SOURCE_HOST'] = 1
            decoded['DESTINATION_MAC'] = decoded['SOURCE_MAC']
            decoded['SOURCE_MAC'] = mac

            #encode message
            encoded = encode_message_dict(decoded)
            push_down(encoded)
          else: #this is a packet that must be rerouted

            #Get IP based on MAC
            ip_tables = open('ip_tables.txt', 'r+')
            try:
                ip = json.loads(ip_tables)
            except:
                #insert router IP first
                router_ip = {'1': 'R'}
                json.dump(router_ip, 'ip_tables.txt')
                json.dump({'IP': 1}, 'ip.txt')

            ip_tables = open('ip_tables.txt', 'r+')
            ips = json.loads(ip_tables)

            try:
              mac = ips[decoded['DESTINATION_HOST']]
              decoded['DESTINATION_MAC'] = mac
              encoded = encode_message_dict(decoded)
              push_down(encoded)
            except:
              #reroute to outside lan
              print('MESSAGE IS FOR OUTSIDE LAN')
        else:
          if decoded['IP_PROTOCOL'] == 'C':
              ip = decoded['DESTINATION_HOST']
              json.dump({'IP': ip}, open('ip.txt','r+'))
          else:
              push_up(decoded)
