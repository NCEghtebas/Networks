from translator import *
from constants import *
import transmit

def encode(message):
    stack = MorseBJStack()
    encoded = stack.encode(message)
    return encoded

def push(encoded_message):
    transmit.get(encoded_message)

def get(ip_protocol, payload, destination):
    dest = encode(destination)
    payload = encode(payload)
    ip_protocol = encode(ip_protocol)
    src = encode(mac)
    sep = [(1,1), (1,0), (3,1), (1,0), (1,1), (1,0), (3,1), (1,0)]
    start = [(20,1),(1,0)]
    stop = [(40,1)]
    push(start + src + sep + dest + sep + ip_protocol + sep + payload + stop)
