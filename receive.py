#
## Introducton to Python breadboarding
#
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
    
    for i in range(blinks):
        print("|{}".format("==" if read_pin(pin) else ""))
        delay(duration)
        
 


if __name__ == "__main__":
    with Safeguards():
       receive()
    
