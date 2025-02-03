import pyvisa

class Instrument:
    def __init__(self) -> None:
        self.connected = False
        pass

    def connect(self, address: str, connection_type: str = 'serial'):
        """
        Establece una conexión con el dispositivo utilizando PyVISA, 
        soportando comunicación serial y GPIB.

        Args:
            address (str): La dirección del dispositivo.
                          - Para 'serial': el puerto serial (por ejemplo, 'COM3', '/dev/ttyUSB0').
                          - Para 'gpib': la dirección GPIB (por ejemplo, 'GPIB0::1::INSTR').
            connection_type (str): El tipo de conexión, 'serial' o 'gpib'. Default es 'serial'.
        """
        
        rm = pyvisa.ResourceManager()
        try:
            if connection_type == 'serial':
                # Conexión serial
                self.connection = rm.open_resource(address, baud_rate=115200, timeout=2000)
                print(f"Conexión serial establecida en el puerto {address}.")
            elif connection_type == 'gpib':
                # Conexión GPIB
                self.connection = rm.open_resource(address)
                self.connection.timeout = 2000  # Configura el timeout (en milisegundos)
                print(f"Conexión GPIB establecida con la dirección {address}.")
            else:
                raise ValueError("Tipo de conexión no soportado. Use 'serial' o 'gpib'.")
        except pyvisa.VisaIOError as e:
            print(f"Error al conectar con {connection_type} en la dirección {address}: {e}")
            self.connection = None
        except ValueError as ve:
            print(ve)
            self.connection = None
