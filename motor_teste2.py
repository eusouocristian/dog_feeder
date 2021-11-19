import RPi.GPIO as GPIO
import time

STEP_PIN = 21
DIR_PIN = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(STEP_PIN, GPIO.OUT) # step
GPIO.setup(DIR_PIN, GPIO.OUT) # Direction


def run_steps():
    
    while True:
        voltas = int(input('Voltas: '))
        steps = voltas*(360/1.8)
        step = 0
        io_level = True
        
        while step < steps:
            if io_level:
                GPIO.output(STEP_PIN, io_level)
                io_level = False
                step += 1
            else:
                GPIO.output(STEP_PIN, io_level)
                io_level = True
                
            time.sleep(0.005)

run_steps()