import time
import math
from servo import Servo, servo2040


"""
Demonstrates how to create a Servo object and control it.
"""

class myServo:
    def __init__(self, serv):
        self.current = 0
                
        self.move_count = 0
        
        self.update_timer = 0
        
        self.running = False
        
        self.init_time = 0
        
        self.move_queue = []
        
        self.step_length = 0
        
        self.queue_index = 0
        
        self.s = Servo(serv)
        self.s.enable()
        
    def set(self, angle):
        self.current = angle
        self.s.value(self.current)

    def disable(self):
        self.s.disable()
        
    def start(self):
        print("Starting que")
        if len(self.move_queue) > 0:
            self.init_time = time.ticks_ms()
            self.update_timer = time.ticks_ms()
            self.running = True
            self.step_length = (self.move_queue[self.queue_index][2] - self.current) / self.move_queue[self.queue_index][1]

    def clearQue(self):
        self.move_queue = []

    def que(self, angle, _time=10, after=0):
        
        num_steps = _time / 10
        
        # Ett steg per 10 ms
        self.step_length = (angle - self.current) / num_steps
        
        self.move_count = 0
                        
        self.move_queue.append([after, num_steps, angle])
    
    def update(self):
        
        
        if self.running: 
            if time.ticks_ms() - self.init_time > self.move_queue[self.queue_index][0]:
                # Implement the logic to update the servo position
                if time.ticks_ms() - self.update_timer > 10:
                    self.update_timer = time.ticks_ms()
                    self.current += self.step_length
                    self.move_count += 1
                
                if self.move_count >= self.move_queue[self.queue_index][1]:
                    print("Move done")
                    self.current = self.move_queue[self.queue_index][2]
                    self.queue_index += 1
                    if self.queue_index >= len(self.move_queue):
                        self.running = False
                        self.s.value(self.current)
                        print("Que done")
                        return
                    self.step_length = (self.move_queue[self.queue_index][2] - self.current) / self.move_queue[self.queue_index][1]
                    self.move_count = 0
                    
                #self.current = self.current + (self.dest - self.current) * 0.05
                self.s.value(self.current)
                
            else:
                self.update_timer = time.ticks_ms()
        
            # Create a numpy array with 10 evenly spaced floats from 0 to 20

