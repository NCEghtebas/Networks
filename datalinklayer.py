from translator import *
from constants import *

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

def decode_header(header, end_header_index):
    sep = [(1,1), (1,0), (3,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
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
        if count == 0:
            decoded_header["SOURCE_LAN"] = d
        elif count == 1:
            decoded_header["SOURCE_HOST"] = d
        elif count == 2:
            decoded_header["DESTINATION_LAN"] = d
        elif count == 3:
            decoded_header["DESTINATION_HOST"] = d
        elif count == 4:
            decoded_header["IP_PROTOCOL"] = d
        elif count == 5:
            decoded_header["CHECKSUM"] = d
        elif count == 6:
            decoded_header["PAYLOAD"] = d
        count += 1
    return decoded_header

def decode_message(message):
    #Declare End Header Sequence
    end_header = [(3,1), (1,0), (1,1), (1,0), (1,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    end_header_indices = find_sub_list(end_header,message)
    end_header_indices = end_header_indices[0]

    #Split message according to header and payload
    header = message[1:end_header_indices[1]+1]
    payload = message[end_header_indices[1]+1:len(message)-1]

    #decode header
    decoded_message = decode_header(header, end_header_indices[0])

    #check if packet is for me or someone else
    #if for someone else, do nothing or reroute packet
    if (decoded_message["DESTINATION_HOST"] != "1"): #CHANGE TO IP
        return decoded_message["DESTINATION_HOST"]

    #Remove Source & Destination information from message
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
    src_lan = "A"
    src_host = '1' #should actually be pulled from router

    message['SOURCE_LAN'] = encode(src_lan)
    message['SOURCE_HOST'] = encode(src_host)
    message["DESTINATION_LAN"] = encode(message["DESTINATION_LAN"])
    message["DESTINATION_HOST"] = encode(message["DESTINATION_HOST"])
    message["IP_PROTOCOL"] = encode(message["IP_PROTOCOL"])
    message['CHECKSUM'] = encode("CHECK") #replace with checksum function
    message["PAYLOAD"] = encode(message["PAYLOAD"])

    #start|stop code for msg and header
    sep = [(1,1), (1,0), (3,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    end_header = [(3,1), (1,0), (1,1), (1,0), (1,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    start = [(20,1),(1,0)]
    stop = [(40,1)]

    push_down(start + message['SOURCE_LAN'] + sep + message['SOURCE_HOST'] + sep + message["DESTINATION_LAN"] + sep + message["DESTINATION_HOST"] + sep + message["IP_PROTOCOL"] + sep + message['CHECKSUM'] + end_header + message["PAYLOAD"] + stop)


def get_from_physical_layer(message):
    decoded = decode_message(message)
    decoded_len = len(decoded)
    mac_address_len = 1
    if decoded_len == mac_address_len:
        print("REROUTE MESSAGE TO IP ADDRESS: " + decoded)
    else:
        push_up(decoded)
