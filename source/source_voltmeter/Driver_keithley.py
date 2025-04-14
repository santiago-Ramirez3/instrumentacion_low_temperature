#import gpib_ctypes
# Asegúrate de poner la ruta correcta del archivo de la biblioteca en el siguiente código.
#gpib_ctypes.gpib.gpib._load_lib('C:\\ruta\\a\\tu\\gpib-32.dll')  # Windows
# gpib_ctypes.gpib.gpib._load_lib('/ruta/a/tu/gpib.so')  # Linux
import pandas as pd
import numpy as np
import pyvisa
import time

def set_up_voltmeter(voltmeter):
    # Configura el voltímetro para medir
    voltmeter.write("F10STX") # Configura el voltímetro
    voltmeter.write("10NX") # Configura el voltímetro

def program_source(source, voltmeter, level, delay, tiempo):
    # Configura el source y mide sus valores junto con el voltímetro
    source.write("REMOTE716") # Configura el source en modo remoto
    source.write("F1,0X") # Configura el source como un source de corriente directa (se debe de enviar dos veces para que el instrumento lo acepte)
    source.write("F1,0X")
    
    source.write(f"B'{level}',0,0X") # Ajusta el nivel del source
    source.write("L100,0X") # Configura la carga del source
    source.write("R1X") # Habilita la entrada de la señal de trigger
    source.write("N1X") # Pone el instrumento en el estado Operate
    source.write("H0X") # Envia la señal del trigger
    source.write("G1,2,0X") # Configura el formato de comunicacion del source con la computadora
    time.sleep(delay) # Espera por el tiempo especificado
    source_measure, volt_measure = medir_source_y_voltmeter(source, voltmeter, tiempo) # Mide 
    return source_measure, volt_measure

def medir_source_y_voltmeter(source, voltmeter, tiempo):
    tiempo_maximo = 0.01 # Define el tiempo máximo de medición en la iteración, para poder tomar varios valores en un intervalo de tiempo antes de pasar al siguiente nivel de corriente
    inicio_tiempo = time.time() # Guarda el tiempo de inicio
    while (time.time() - inicio_tiempo) < tiempo_maximo: # Ejecuta el bucle hasta que pase el tiempo máximo
        time.sleep(0.01) # Espera por 0.01 segundos para empezar
        tiempo_actual = time.time() - tiempo # Calcula el tiempo actual
        BUFFER_source = float(source.query("*IDN?")) # Lee el valor del source
        print("valor medido del source:", BUFFER_source)
        BUFFER_voltmeter = float(voltmeter.query("*IDN?")) # Lee el valor del voltímetro
        print("valor medido del voltímetro:", BUFFER_voltmeter)
    return BUFFER_source, BUFFER_voltmeter

def connect_intruments(source_address, voltmeter_address):
    try:
        rm = pyvisa.ResourceManager() # Crea un administrador de recursos dePyVISA
        voltmeter = rm.open_resource(voltmeter_address) # Abre el recurso delvoltímetro
        source = rm.open_resource(source_address) # Abre el recurso delsource

        return source, voltmeter
    except Exception:
        print(Exception)

def close_instruments(source, voltmeter):
    try:
        source.close()
        voltmeter.close()
    except Exception:
        print(Exception)

def current_sweep(initialC, finalC, stepC, source, voltmeter):

    current_values = np.arange(initialC, finalC, stepC)

    # Delay de espera para que el voltmeter tome el dato una vez seestablece el nivel en el source
    delay = 1

    tiempo = time.time() # Obtiene el tiempo actual
    # Bucle para programar el source y medir
    for i in current_values:
        level = i # Incrementa el nivel del source
        program_source(source, voltmeter, level, delay,tiempo) # Programa y mide
        print(i)

def main():
    voltmeter_address = 'GPIB0::22::INSTR' # Dirección del voltímetro
    source_address = 'GPIB0::16::INSTR' # Dirección del source

    source, voltmeter = connect_intruments(source_address, voltmeter_address)
    

    # Configuración de los parámetros iniciales del valor donde inicia elsource, el paso en cada iteración y el valor final
    initialC = 0.00000001
    finalC =   0.0000001
    stepC =   0.00000001 
    
    set_up_voltmeter(voltmeter) # Configura el voltímetro

    current_sweep(initialC, finalC, stepC, source, voltmeter)

    # Cierra las comunicaciones con los equipos de medición
    close_instruments(source, voltmeter)

if __name__ == "__main__":
    main() # Ejecuta la función principal