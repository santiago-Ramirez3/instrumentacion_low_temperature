#import gpib_ctypes
# Asegúrate de poner la ruta correcta del archivo de la biblioteca en el siguiente código.
#gpib_ctypes.gpib.gpib._load_lib('C:\\ruta\\a\\tu\\gpib-32.dll')  # Windows
# gpib_ctypes.gpib.gpib._load_lib('/ruta/a/tu/gpib.so')  # Linux
import pandas as pd
import pyvisa
import time

def programar_generador(generador, voltimetro, df, level, delay, tiempo):
     # Configura el generador y mide sus valores junto con el voltímetro
     generador.write("REMOTE716") # Configura el generador en modo remoto
     generador.write("F1,0X") # Configura el generador como un generador de corriente directa (se debe de enviar dos veces para que el instrumento lo acepte)
     generador.write("F1,0X")

     generador.write(f"B'{level}',0,0X") # Ajusta el nivel del generador
     generador.write("L100,0X") # Configura la carga del generador
     generador.write("R1X") # Habilita la entrada de la señal de trigger
     generador.write("N1X") # Pone el instrumento en el estado Operate
     generador.write("H0X") # Envia la señal del trigger
     generador.write("G1,2,0X") # Configura el formato de comunicacion del generador con la computadora
     time.sleep(delay) # Espera por el tiempo especificado
     df = medir_generador_y_voltimetro(generador, voltimetro, df, tiempo) # Mide y actualiza el DataFrame
     return df # Retorna el DataFrame actualizado

def programar_voltimetro(voltimetro):
     # Configura el voltímetro para medir
     voltimetro.write("F10STX") # Configura el voltímetro
     voltimetro.write("10NX") # Configura el voltímetro

def medir_generador_y_voltimetro(generador, voltimetro, df, tiempo):
     tiempo_maximo = 0.01 # Define el tiempo máximo de medición en la iteración, para poder tomar varios valores en un intervalo de tiempo antes de pasar al siguiente nivel de corriente
     inicio_tiempo = time.time() # Guarda el tiempo de inicio
     while (time.time() - inicio_tiempo) < tiempo_maximo: # Ejecuta el bucle hasta que pase el tiempo máximo
         time.sleep(0.01) # Espera por 0.01 segundos para empezar
         tiempo_actual = time.time() - tiempo # Calcula el tiempo actual
         BUFFER_generador = float(generador.query("*IDN?")) # Lee el valor del generador
         print("valor medido del generador:", BUFFER_generador)
         BUFFER_voltimetro = float(voltimetro.query("*IDN?")) # Lee el valor del voltímetro
         print("valor medido del voltímetro:", BUFFER_voltimetro)
    
         # Crea un nuevo DataFrame con los datos actuales

         new_data = pd.DataFrame({'Tiempo': [tiempo_actual], 'Valor_generador': [BUFFER_generador], 'Valor_voltimetro':[BUFFER_voltimetro]})
         df = pd.concat([df, new_data], ignore_index=True) # Agrega losnuevos datos al DataFrame original

     return df # Retorna el DataFrame actualizado

def main():
     rm = pyvisa.ResourceManager() # Crea un administrador de recursos dePyVISA
     voltimeter_address = 'GPIB0::22::INSTR' # Dirección del voltímetro
     generator_address = 'GPIB0::16::INSTR' # Dirección del generador
     voltimetro = rm.open_resource(voltimeter_address) # Abre el recurso delvoltímetro
     generador = rm.open_resource(generator_address) # Abre el recurso delgenerador

     # Configuración de los parámetros iniciales del valor donde inicia elgenerador, el paso en cada iteración y el valor final
     inicio = 0.00000001
     stop = 0.0000001
     step = 0.00000001
     # Delay de espera para que el voltimetro tome el dato una vez seestablece el nivel en el generador
     delay = 1
     # Valores establecidos para el for

     inicio_int = int(inicio * 100000000)
     stop_int = int(stop * 100000000)
     step_int = int(step * 100000000)
     # Crea un DataFrame vacío con las columnas especificadas
     df = pd.DataFrame(columns=['Tiempo', 'Valor_generador','Valor_voltimetro'])
     level = inicio
     tiempo = time.time() # Obtiene el tiempo actual
     programar_voltimetro(voltimetro) # Configura el voltímetro
     # Configuración de las gráficas
     # Bucle para programar el generador y medir
     for i in range(inicio_int, stop_int, step_int):
         level = level + step # Incrementa el nivel del generador
         df = programar_generador(generador, voltimetro, df, level, delay,tiempo) # Programa y mide
         print(i)
     # Cierra las comunicaciones con los equipos de medición
     voltimetro.close()
     generador.close()

if __name__ == "__main__":
     main() # Ejecuta la función principal