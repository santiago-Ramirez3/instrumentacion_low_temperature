import pyvisa
from serial.tools import list_ports

def list_available_ports() -> list:
    """
    Genera una lista de los puertos seriales disponibles y las direcciones GPIB detectadas.
    
    Returns:
        dict: Un diccionario con las claves 'serial_ports' y 'gpib_addresses'.
              - 'serial_ports' contiene una lista de puertos seriales disponibles.
              - 'gpib_addresses' contiene una lista de direcciones GPIB disponibles.
    """
    # Obtener los puertos seriales disponibles
    serial_ports = [port.device for port in list_ports.comports()]

    # Obtener las direcciones GPIB y otros recursos VISA
    rm = pyvisa.ResourceManager()
    visa_resources = rm.list_resources()
    
    # Filtrar las direcciones GPIB
    gpib_addresses = [resource for resource in visa_resources if 'GPIB' in resource]

    return serial_ports + gpib_addresses

print(list_available_ports())