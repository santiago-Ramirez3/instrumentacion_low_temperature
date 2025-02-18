from drivers import Instrument

class Power_supply(Instrument):
    def __init__(self) -> None:
        self.instrumentClass = 'Power supply'
        self.name = 'Keithley2450'
        super().__init__()