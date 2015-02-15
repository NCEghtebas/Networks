from translator import *
from constants import *
from transmit import get_from_datalink_layer

def encode(message):
    stack = MorseBJStack()
    encoded = stack.encode(message)
    return encoded

def decode(message):
    stack = MorseBJStack()
    #stack = BJStack([MsgLetterLayer(), LetterMorseLayer(), MorseSignalLayer()])
    #decoded = stack.decode(message)
    return message

def push_down(encoded_message):
    get_from_datalink_layer(encoded_message)

def get_from_ip_layer(ip_protocol, payload, destination):
    dest = encode(destination)
    payload = encode(payload)
    ip_protocol = encode(ip_protocol)
    src = encode(mac)
    sep = [(1,1), (1,0), (3,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    end_header = [(3,1), (1,0), (1,1), (1,0), (1,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    start = [(20,1),(1,0)]
    stop = [(40,1)]
    push_down(start + src + sep + dest + sep + ip_protocol + end_header + payload + stop)


def get_from_physical_layer(message):
    decoded = decode(message)
    print(decoded)
    #push up
