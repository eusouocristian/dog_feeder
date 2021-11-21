import RPi.GPIO as GPIO
import time

STEP_PIN = 18
EN_PIN = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(STEP_PIN, GPIO.OUT) # step
GPIO.setup(EN_PIN, GPIO.OUT) # Direction
GPIO.output(EN_PIN, 0) # Disable output with 1
pwm0 = GPIO.PWM(STEP_PIN, 1000)
pwm0.start(50)

io_level = True

while True:
	if io_level:
		GPIO.output(STEP_PIN, io_level)
		io_level = False
	else:
		GPIO.output(STEP_PIN, io_level)
		io_level = True
	time.sleep(0.005)
