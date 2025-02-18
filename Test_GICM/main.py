from source_voltmeter import Driver_keithley as sv
from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td

import numpy as np
import time

motor_port = "COM12"
motor = md.connect_to_arduino(motor_port)

thermometers_port = "COM5"
thermometers = td.connect_to_arduino(thermometers_port)

voltmeter_address = 'GPIB0::22::INSTR' # Dirección del voltímetro
source_address = 'GPIB0::16::INSTR' # Dirección del source

source, voltmeter = sv.connect_intruments(source_address, voltmeter_address)

#----------------------------------------------------------------------------

initialC = 0.0
finalC = 2.4e-2
setpC = 2.4e-3

currents = np.arange(initialC, finalC, setpC)

delay = 1

tiempo = time.time() # Obtiene el tiempo actual
# Bucle para programar el source y medir
for i in currents:
    level = i # Incrementa el nivel del source
    sv.programar_source(source, voltmeter, level, delay,tiempo) # Programa y mide
    print("Current: ",i)

    temp1, temp2 = td.query_temperatures(thermometers)
    print(f"Temperature 1: {temp1} °C, Temperature 2: {temp2} °C")

    md.send_movement_command(motor, "-20")

md.send_movement_command(motor, "1000")

md.close_connection(motor)
td.close_connection(thermometers)
sv.close_instruments(source, voltmeter)

