# Import file from folders to control the devices
from source_voltmeter import Driver_keithley as sv
from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td

# Import libreries
import pandas as pd
import numpy as np
import time

motor_port = "COM14" # Port for Arduino connected to step motor
motor = md.connect_to_arduino(motor_port) # Create the connection

voltmeter_address = 'GPIB0::22::INSTR' # Voltmeter GPIB address
source_address = 'GPIB0::16::INSTR' # Source GPIB address

source, voltmeter = sv.connect_intruments(source_address, voltmeter_address) # create separated instrument objects

#----------------------------------------------------------------------------


# Define  initial, final and current step un Amperes
initialC = 0.0 
finalC = 2.0e-2


#currents = np.arange(initialC, finalC, setpC) # numerical array with all current value
currents1 = np.linspace(initialC, finalC, 10)
delay = 1

tiempo = time.time() # Obtiene el tiempo actual

md.send_movement_command(motor, "1000") # Get up the system
md.wait_for_movement_to_complete(motor)
time.sleep(3)
#md.send_movement_command(motor, "-1000") # Get up the system
#md.wait_for_movement_to_complete(motor)
#time.sleep(15)
print("iniciando toma de datos")
#----------------------------------------------------------------------------

# Create an empty DataFrame to store the measurements
columns = ["Current", "Source Measure", "Volt Measure", "Timestamp"]
data = pd.DataFrame(columns=columns)

for i in currents1:
    level = i  # Set the source level
    
    # Program and measure
    source_measure, volt_measure = sv.program_source(source, voltmeter, level, delay, tiempo)

    # Capture timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Append the new measurement to the DataFrame
    data = pd.concat([data, pd.DataFrame([[level, source_measure, volt_measure, timestamp]], columns=columns)], ignore_index=True)

    time.sleep(1)

# Save to CSV
data.to_csv("measurements_6.csv", index=False)
print("Measurements saved to measurements.csv")


#----------------------------------------------------------------------------

# Finish the protocol

sv.program_source(source, voltmeter, 0.0, delay,tiempo) # set source at 0.0 amperes

md.send_movement_command(motor, "1000") # Get up the system

# close all connections
md.close_connection(motor)
sv.close_instruments(source, voltmeter)

