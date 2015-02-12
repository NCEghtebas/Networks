import time
import RPi.GPIO as GPIO
from translator import *

class Safeguards:
    def __enter__(self):
        return self
    def __exit__(self,*rabc):
        GPIO.cleanup()
        print("Safe exit succeeded")
        return not any(rabc)

def prepare_pin(pin=17):
    GPIO.setmode(GPIO.BCM)  #use Broadcom (BCM) GPIO numbers on breakout pcb

    GPIO.setup(pin,GPIO.OUT) # allow pi to set 3.3v and 0v levels

def turn_high(pin=17):
    GPIO.output(pin,GPIO.HIGH)  # set 3.3V level on GPIO output

def turn_low(pin=17):
    GPIO.output(pin,GPIO.LOW)   # set ground (0) level on GPIO output

def delay(duration):            # sleep for duration seconds where duration is a float.
    time.sleep(duration)

def transmit(pulses, duration=1/100, pin=17):
    prepare_pin(pin)
    for pulse in pulses:
        if pulse[1]:
            turn_high(pin)
        else:
            turn_low(pin)
        delay(duration * pulse[0])
    turn_low(pin)

def main():
    stack = MorseBJStack()
    message = input('Enter Message: ')

    encoded = [(20,1),(1,0)] + stack.encode(message) + [(40,1)]

    print("{}".format(encoded))

    transmit(encoded)

if __name__ == "__main__":
    with Safeguards():
        main()
