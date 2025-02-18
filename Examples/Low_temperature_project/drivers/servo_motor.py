from drivers import Instrument

class Servo_motor(Instrument):
    def __init__(self):
        self.instrumentClass = 'servo motor'
        self.name = 'servo motor 1'
        super().__init__()