# Get the parent directory of the current script to import objects from source folder
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# Import file from folders to control the devices
from source.source_voltmeter import Driver_keithley as sv
from source.step_by_step_motor import motor_drive as md
from source.temperature_sensors import thermometers_driver as td

from source.predefined_protocols.temperature_reaching import reach_temperature_PID
from source.predefined_protocols.power_supply import current_curve

# Import libreries
import pandas as pd
import numpy as np
import time


#===================================================================================================
# Parameters for the experiment

# Device connections
motor_port = "COM14"  # Port for Arduino connected to step motor
thermometers_port = "COM13"  # Port for thermometers
voltmeter_address = 'GPIB0::22::INSTR' # Voltmeter GPIB address
source_address = 'GPIB0::16::INSTR' # Source GPIB address

initial_height = 1000     # Starting (absolute) height

#===================================================================================================

# Device connections
motor = md.connect_to_arduino(motor_port)  # Create the motor connection
thermometers = td.connect_to_arduino(thermometers_port)  # Create the thermometers connection
source, voltmeter = sv.connect_intruments(source_address, voltmeter_address) # create separated instrument objects

# ------------------------------------------------------------------------------------
# Initialize system position

# Move system to starting position
print("Moving system to initial height...")
md.send_movement_command(motor, str(initial_height))
response = md.wait_for_movement_to_complete(motor)
time.sleep(2)
md.send_movement_command(motor, str("-250"))        # move 450 mm
response = md.wait_for_movement_to_complete(motor)
time.sleep(10)
# ------------------------------------------------------------------------------------

temperature_list = np.arange(-160,-220,-20)

for temp in temperature_list:
    reach_temperature_PID(target_temperature = temp, thermometers = thermometers, motor = motor)

    current_curve(folder="Experiment_LED_RED",
                  name="whatever",
                  temperature=temp,
                  source=source,
                  voltmeter=voltmeter,
                  initialC=0.0,
                  finalC=0.025,
                  nMeasures=30)

# ------------------------------------------------------------------------------------
# Optional: Return system to the starting position
print("PID control loop completed. Returning system to initial height...")
# ------------------------------------------------------------------------------------

md.send_movement_command(motor, "1000") # Get up the system

# close all connections
md.close_connection(motor)
sv.close_instruments(source, voltmeter)
