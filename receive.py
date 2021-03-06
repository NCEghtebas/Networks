#
## Introducton to Python breadboarding
#
import time
import RPi.GPIO as GPIO
from translator import *
import math

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

def push_up(pulses):
    from datalinklayer import get_from_physical_layer
    get_from_physical_layer(pulses)
    

def main():
    stack = MorseBJStack()
    pulses = receive()
    #from threading import Thread
    #listen_thread = Thread(target=push_up, args=(pulses))
    #listen_thread.start()
    push_up(pulses)

if __name__ == "__main__":
    with Safeguards():
       main()
