from drivers import Instrument
import pyvisa

class Thermometer(Instrument):
    def __init__(self) -> None:
        self.instrumentClass = 'Thermometer'
        self.connection = None  # Para almacenar la conexión PyVISA
        super().__init__()

    def connect(self, port: str):
        """
        Establece una conexión con el termómetro a través de un puerto serial usando PyVISA.
        
        Args:
            port (str): El puerto serial (por ejemplo, 'COM3', '/dev/ttyUSB0').
        """
        rm = pyvisa.ResourceManager()
        try:
            # Abre conexión al puerto serial
            self.connection = rm.open_resource(port, baud_rate=115200, timeout=2000)
            print(f"Conexión establecida con el termómetro en el puerto {port}.")
        except pyvisa.VisaIOError as e:
            print(f"Error al conectar con el puerto {port}: {e}")
            self.connection = None

    def read(self):
        """
        Envía el comando 'm' al termómetro para leer la temperatura y devuelve el resultado.

        Returns:
            str: Lectura de la temperatura desde el termómetro.
        """
        if not self.connection:
            raise ConnectionError("No se ha establecido una conexión. Usa el método connect primero.")

        try:
            # Enviar comando 'm' para iniciar la medición
            self.connection.write('T')
            
            # Leer la respuesta del termómetro
            response = self.connection.read()
            return response.strip()  # Eliminar espacios en blanco o saltos de línea innecesarios
        except pyvisa.VisaIOError as e:
            print(f"Error al leer del termómetro: {e}")
            return None