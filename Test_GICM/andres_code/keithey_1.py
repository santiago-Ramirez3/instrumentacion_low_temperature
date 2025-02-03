import pyvisa
import time
import pandas as pd
from openpyxl.chart import ScatterChart, Series, Reference
#from pt100_serial import PT100_serial
import matplotlib.pyplot as plt

def programar_generador(generador, voltimetro, df, level, delay, tiempo,temperatura, ax, a2x, line, line2):
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
     df = medir_generador_y_voltimetro(generador, voltimetro, df, tiempo, temperatura, ax, a2x, line, line2) # Mide y actualiza el DataFrame
     return df # Retorna el DataFrame actualizado

def programar_voltimetro(voltimetro):
     # Configura el voltímetro para medir
     voltimetro.write("F10STX") # Configura el voltímetro
     voltimetro.write("10NX") # Configura el voltímetro

def medir_generador_y_voltimetro(generador, voltimetro, df, tiempo, temperatura, ax, a2x, line, line2):
     tiempo_maximo = 0.01 # Define el tiempo máximo de medición en la iteración, para poder tomar varios valores en un intervalo de tiempo antes de pasar al siguiente nivel de corriente
     inicio_tiempo = time.time() # Guarda el tiempo de inicio
     while (time.time() - inicio_tiempo) < tiempo_maximo: # Ejecuta el bucle hasta que pase el tiempo máximo
         time.sleep(0.01) # Espera por 0.01 segundos para empezar
         tiempo_actual = time.time() - tiempo # Calcula el tiempo actual
         BUFFER_generador = float(generador.query("*IDN?")) # Lee el valor del generador
         print("valor medido del generador:", BUFFER_generador)
         BUFFER_voltimetro = float(voltimetro.query("*IDN?")) # Lee el valor del voltímetro
         print("valor medido del voltímetro:", BUFFER_voltimetro)
         temp = temperatura.read_temp() # Lee la temperatura
         td = temp['td'] if temp else None # Obtiene la temperatura enviadapor el sensor
         print("valor medido de la temperatura:", td)
    
         # Crea un nuevo DataFrame con los datos actuales

         new_data = pd.DataFrame({'Tiempo': [tiempo_actual], 'Valor_generador': [BUFFER_generador], 'Valor_voltimetro':[BUFFER_voltimetro], 'Valor_temperatura': [td]})
         df = pd.concat([df, new_data], ignore_index=True) # Agrega losnuevos datos al DataFrame original
    
         # Actualiza la gráfica en tiempo real
         ax.clear()
         ax.plot(df['Valor_voltimetro'], df['Valor_generador'], label='Generador')
         ax.legend()
         line.set_data(df['Valor_voltimetro'], df['Valor_generador'])
         a2x.clear()
         a2x.plot(df['Tiempo'], df['Valor_temperatura'], label='Temperatura')
         a2x.legend()
         line2.set_data(df['Tiempo'], df['Valor_temperatura'])
         plt.pause(0.00001)
     return df # Retorna el DataFrame actualizado

def main():
     rm = pyvisa.ResourceManager() # Crea un administrador de recursos dePyVISA
     voltimeter_address = 'GPIB0::22::INSTR' # Dirección del voltímetro
     generator_address = 'GPIB0::16::INSTR' # Dirección del generador
     voltimetro = rm.open_resource(voltimeter_address) # Abre el recurso delvoltímetro
     generador = rm.open_resource(generator_address) # Abre el recurso delgenerador
     nombre_de_la_hoja= 'primera' # Nombre de la hoja en Excel
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
     df = pd.DataFrame(columns=['Tiempo', 'Valor_generador','Valor_voltimetro', 'Valor_temperatura'])
     level = inicio
     tiempo = time.time() # Obtiene el tiempo actual
     temperatura = PT100_serial("COM9") # Asigna el objeto a ´´temperatura´´y se inserta el valor del puerto USB donde se conectó el sensor
     temperatura.conectar() # Conecta el sensor de temperatura
     programar_voltimetro(voltimetro) # Configura el voltímetro
     # Configuración de las gráficas
     fig, ax = plt.subplots()
     line, = ax.plot([], [])
     plt.xlabel('voltaje')
     plt.ylabel('corriente')
     plt.title('Mediciones en tiempo real')
     fig2, a2x = plt.subplots()
     line2, = a2x.plot([], [])
     plt.xlabel('tiempo')
     plt.ylabel('temperatura')
     plt.title('Mediciones en tiempo real')
     # Bucle para programar el generador y medir
     for i in range(inicio_int, stop_int, step_int):
         level = level + step # Incrementa el nivel del generador
         df = programar_generador(generador, voltimetro, df, level, delay,tiempo, temperatura, ax, a2x, line, line2) # Programa y mide
         print(i)
     # Cierra las comunicaciones con los equipos de medición
     voltimetro.close()
     generador.close()
     # Calcula promedios de las mediciones
     promedio_generador = df['Valor_generador'].mean()
     promedio_voltimetro = df['Valor_voltimetro'].mean()
     promedio_temperatura = df['Valor_temperatura'].mean()
     resistencia = promedio_voltimetro / promedio_generador # Calcula laresistencia

     print("valor de la resistencia:", resistencia)
     print('Valor de la temperatura:', promedio_temperatura)
     # Guarda los datos en un archivo de Excel
     with pd.ExcelWriter('measurement_data_pandas.xlsx', mode='a', engine='openpyxl', if_sheet_exists='new') as writer:
         df.to_excel(writer, sheet_name=f'{nombre_de_la_hoja}', index=False)
# Escribe los datos en Excel
         sheet = writer.sheets[f'{nombre_de_la_hoja}']
         # Crea un gráfico de dispersión para los valores del generador y elvoltímetro
         chart = ScatterChart()
         chart.title = f"Voltaje vs corriente\nTemp:{promedio_temperatura:.2f}°C\nResistencia: {resistencia:.2f}Ω"
         chart.style = 13
         chart.x_axis.title = 'Valor del Generador'
         chart.y_axis.title = 'Valor del Voltimetro'
         yvalues = Reference(sheet, min_col=2, min_row=2, max_row=len(df) + 1)
         xvalues = Reference(sheet, min_col=3, min_row=2, max_row=len(df) + 1)
         series = Series(xvalues, yvalues, title_from_data=True)
         chart.series.append(series)
         sheet.add_chart(chart, "E5")
     plt.show() # Muestra las gráficas
if __name__ == "__main__":
     main() # Ejecuta la función principal