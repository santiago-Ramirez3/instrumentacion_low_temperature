from experiments import Experimetn
from drivers.servo_motor import Servo_motor
from drivers.thermometer import Thermometer
from drivers.power_supply import Power_supply

thermo = Thermometer()
servo = Servo_motor()
power = Power_supply()

instruments = [thermo, servo, power]

def protocol():
    try:
        with open() as f:
            f.read()

    except Exception as e:
        print(e)
    pass


class ohm_law_temperature(Experimetn):
    def __init__(self, starting_criteria: bool, end_criteria: bool, saving_path: str):
        super().__init__(instruments, starting_criteria, end_criteria, protocol, saving_path)


    
    
