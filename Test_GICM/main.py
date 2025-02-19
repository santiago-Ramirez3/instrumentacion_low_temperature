# Import file from folders to control the devices
from source_voltmeter import Driver_keithley as sv
from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td

# Import libreries
import numpy as np
import time

motor_port = "COM12" # Port for Arduino connected to step motor
motor = md.connect_to_arduino(motor_port) # Create the connection

thermometers_port = "COM5" # Port for thermometers
thermometers = td.connect_to_arduino(thermometers_port) # Create the connection

voltmeter_address = 'GPIB0::22::INSTR' # Voltmeter GPIB address
source_address = 'GPIB0::16::INSTR' # Source GPIB address

source, voltmeter = sv.connect_intruments(source_address, voltmeter_address) # create separated instrument objects

#----------------------------------------------------------------------------

# Define  initial, final and current step un Amperes
initialC = 0.0 
finalC = 2.4e-2
setpC = 2.4e-3

currents = np.arange(initialC, finalC, setpC) # numerical array with all current value

delay = 1

tiempo = time.time() # Obtiene el tiempo actual

md.send_movement_command(motor, "1000") # Get up the system
md.wait_for_movement_to_complete(motor)
#----------------------------------------------------------------------------

# Loop to do the experimental measures at each step
for i in currents:
    level = i # Incrementa el nivel del source
    sv.program_source(source, voltmeter, level, delay,tiempo) # Programa y mide

    temp1, temp2 = td.query_temperatures(thermometers)
    print(f"Temperature 1: {temp1} °C, Temperature 2: {temp2} °C")

    md.send_movement_command(motor, "-20")
#----------------------------------------------------------------------------

# Finish the protocol

sv.program_source(source, voltmeter, 0.0, delay,tiempo) # set source at 0.0 amperes

md.send_movement_command(motor, "1000") # Get up the system

# close all connections
md.close_connection(motor)
td.close_connection(thermometers)
sv.close_instruments(source, voltmeter)

