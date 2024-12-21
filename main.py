import time
import random
from ServoHandler import myServo
from servo import Servo, servo2040
from machine import Pin
from pimoroni import Analog, AnalogMux

"""
Demonstrates how to create a Servo object and control it.
""" 

servos = [myServo(servo2040.SERVO_1), 
          myServo(servo2040.SERVO_2), 
          myServo(servo2040.SERVO_3), 
          myServo(servo2040.SERVO_4), 
          myServo(servo2040.SERVO_5), 
          myServo(servo2040.SERVO_6), 
          myServo(servo2040.SERVO_7), 
          myServo(servo2040.SERVO_8)]


servos[0].set(0)

servos[0].que(100, 2000, 0)
servos[0].que(0, 2000, 3000)
servos[0].que(170, 4000, 5000)
servos[0].que(0, 1000, 10000)

#Pilla inte på något nedanför ----------------------
mux = AnalogMux(servo2040.ADC_ADDR_0, servo2040.ADC_ADDR_1, servo2040.ADC_ADDR_2,
                muxed_pin=Pin(servo2040.SHARED_ADC))

read_adc = Analog(servo2040.SHARED_ADC)

mux.configure_pull(servo2040.SENSOR_1_ADDR, Pin.PULL_DOWN)
mux.select(servo2040.SENSOR_1_ADDR)

button_listening = True

all_running = True
while all_running:
    
    if button_listening:
        if round(read_adc.read_voltage(), 3) > 3.0:
            for a in servos:
                a.start()
            button_listening = False
    else:
        num_running = 0
        
        # Read each sensor in turn and print its voltage

        #update all
        for a in servos:
            a.update()
            if a.running:
                num_running += 1
        
        if num_running == 0:
            all_running = False
    
print("All done")
    
for a in servos:
    a.disable()