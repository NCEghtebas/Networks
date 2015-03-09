import time
import RPi.GPIO as GPIO
import math
import sys
from translator import *

#import sys
#sys.path.insert(0, '')
#import imp
#translator = imp.load_source('translator.py', '../translator.py')


class Safeguards:
    def __enter__(self):
        return self
    def __exit__(self,*rabc):
        GPIO.cleanup()
        print("Safe exit succeeded")
        return not any(rabc)

def prepare_pin(pin=23):
    GPIO.setmode(GPIO.BCM)  #use Broadcom (BCM) GPIO numbers on breakout pcb

    GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # allow pi to read levels

def read_pin(pin):
    return GPIO.input(pin)  # set 3.3V level on GPIO output

def delay(duration):            # sleep for duration seconds where duration is a float.
    time.sleep(duration)

def receive(duration=1/1000,pin=23):
    prepare_pin(pin)
    ratio = 10
    pulses = []
    am_reading = False
    count = 0
    last = 0
    while (True):
        current = read_pin(pin)
        read_pulse = (math.ceil(count/ratio), last)

        if (current != last):
            if (read_pulse[0] > 10 and read_pulse[0] <= 20 and read_pulse[1]):
                #start reading sequence
                am_reading = True
                pulses = []
            elif (read_pulse[0] >= 30 and read_pulse[1]):
                #stop reading
                am_reading = False
                return pulses
            else:
                if (am_reading):
                    if (read_pulse[0] == 2 or read_pulse[0] == 6):
                        read_pulse = (read_pulse[0] + 1, last)
                    pulses.append(read_pulse)
            count = 0
        else:
            count += 1
        last = current
        delay(duration)

def route_to_pi (message):
    from transmit_router import transmit
    
    print("PULSES: " + str(message))
    decoded = decode_message(message)
    transmit(decoded)

# Decoding

def decode(message):
    stack = MorseBJStack()
    encoded = stack.decode(message)
    return encoded

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
    print("DECODED: " + str(decoded_message))
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

def assign_ip():
    pass

def main():
    stack = MorseBJStack()
    pulses = receive()

    # assign IP
    
    # check destination

    # send message to correct Pi

if __name__ == "__main__":
    with Safeguards():
       main()
