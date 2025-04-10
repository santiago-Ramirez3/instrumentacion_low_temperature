from source_voltmeter import Driver_keithley as sv
from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td

import pandas as pd
import numpy as np
import time
import threading

def current_curve(color, temperature, source, voltmeter, initialC, finalC, nMeasures):
    currents = np.linspace(initialC, finalC, nMeasures)
    delay = 1
    tiempo = time.time()

    print("Starting electrical measurements...")
    
    columns = ["Current", "Source Measure", "Volt Measure", "Timestamp", "Temperature"]
    data = pd.DataFrame(columns=columns)
    
    for i in currents:
        level = i  # Set the source level
        
        source_measure, volt_measure = sv.program_source(source, voltmeter, level, delay, tiempo)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        data = pd.concat([data, pd.DataFrame([[level, source_measure, volt_measure, timestamp, temperature]], columns=columns)], ignore_index=True)
        
        time.sleep(1)
    
    filename = f"measurements_green_{temperature}.csv"
    data.to_csv(filename, index=False)
    print(f"Measurements saved to {filename}")
    
    sv.program_source(source, voltmeter, 0.0, delay, tiempo)  # Reset source to 0A

def monitor_temperature(thermometers):
    last_temps = []
    acclimation_tolerance = 0.5
    while True:
        temp1, temp2 = td.query_temperatures(thermometers)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} | Temp1: {temp1}°C | Temp2: {temp2}°C")
        
        last_temps.append(temp1)
        if len(last_temps) > 8:
            last_temps.pop(0)
        
        if len(last_temps) == 8 and np.max(np.abs(np.diff(last_temps))) < acclimation_tolerance:
            print("Temperature stabilized.")
        else:
            print("Temperature not yet stabilized.")
        
        time.sleep(5)

def manual_control_loop(thermometers, motor, source, voltmeter):
    print("Manual control mode started. Enter movement values or type 'measure' to start measurements.")
    threading.Thread(target=monitor_temperature, args=(thermometers,), daemon=True).start()
    
    while True:
        command = input("Enter movement value (positive to move up, negative to move down) or 'measure' to start measurement: ")
        
        if command.lower() == 'measure':
            color = input("Enter color identifier: ")
            temp = td.query_temperatures(thermometers)[0]  # Use the current temperature reading
            current_curve(color, temp, source, voltmeter, initialC=0.0, finalC=2.0e-2, nMeasures=10)
        elif command.replace('-', '').isdigit():
            movement = int(command)
            md.send_movement_command(motor, str(movement))
            response = md.wait_for_movement_to_complete(motor)
            print(f"Motor response: {response}")
        else:
            print("Invalid input. Please enter a number or 'measure'.")

# Device connections
motor = md.connect_to_arduino("COM19")
thermometers = td.connect_to_arduino("COM20")
source, voltmeter = sv.connect_intruments('GPIB0::16::INSTR', 'GPIB0::22::INSTR')

print("Moving system to initial height...")
md.send_movement_command(motor, "1000")
md.wait_for_movement_to_complete(motor)
time.sleep(2)
md.send_movement_command(motor, "-430")
md.wait_for_movement_to_complete(motor)
time.sleep(10)

manual_control_loop(thermometers, motor, source, voltmeter)

print("Returning system to initial height...")
md.send_movement_command(motor, "1000")
md.close_connection(motor)
sv.close_instruments(source, voltmeter)
