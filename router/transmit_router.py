import time
import RPi.GPIO as GPIO
import math
import sys

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

def transmit(message):
    address = message["DESTINATION_LAN"] + decoded["DESTINATION_HOST"]

def encode(message):

def main():
    stack = MorseBJStack()

if __name__ == "__main__":
    with Safeguards():
       main()
