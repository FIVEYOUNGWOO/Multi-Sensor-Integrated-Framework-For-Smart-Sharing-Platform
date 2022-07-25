## sudo pigpiod
## Use Deamon
import pigpio
import time

class ServoCls:
    """
    ServoMotor Control Class
    Red     +
    Brown   -
    Orange  Control
    """
    def __init__(self):
        self.ServoPin = [
            [18, 23]       # left  | right pin
        ]        
        self.Angle = [
            ##
            # 500  -> 0도
            # 2500 -> 180도
            [           # first Hole
                [1100, 1800],     # open Angle      left  | right pin
                [1800, 1100]      # close Angle     left  | right pin
            ]
        ]
        self.pi = pigpio.pi()
    
    def _act(self, pin, angle):
        print(pin, angle)
        self.pi.set_servo_pulsewidth(pin, angle)

    def Open(self, hole = 1):
        self._act(self.ServoPin[hole - 1][0], self.Angle[hole - 1][0][0])
        self._act(self.ServoPin[hole - 1][1], self.Angle[hole - 1][0][1])

    def Close(self, hole = 1):
        self._act(self.ServoPin[hole - 1][0], self.Angle[hole - 1][1][0])
        self._act(self.ServoPin[hole - 1][1], self.Angle[hole - 1][1][1])

    def Act(self, IsOpen, hole = 1):
        if IsOpen:
            self.Open(hole)
        else:
            self.Close(hole)
