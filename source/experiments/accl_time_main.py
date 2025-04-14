from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td
import pandas as pd
import numpy as np
import time

# Device connections
motor_port = "COM14"
motor = md.connect_to_arduino(motor_port)

thermometers_port = "COM13"
thermometers = td.connect_to_arduino(thermometers_port)

# Experiment Parameters
initial_height = 1000   # Starting height
aim_height = 350        # Target height
step_size = 1000 - aim_height
acclimation_tolerance = 0.3  # Temperature stabilization tolerance
movement_speed = 20  # Estimated speed (units per second)
estimated_movement_time = abs(step_size) / movement_speed

# Data storage
data = []  # Combined storage for thermometer 1 (ambient) and thermometer 2 (water)

# Move system to initial height
time.sleep(1)
md.send_movement_command(motor, str(initial_height))
md.wait_for_movement_to_complete(motor)
time.sleep(2)

# Move system down to the desired height
md.send_movement_command(motor, str(-step_size))
md.wait_for_movement_to_complete(motor)
time.sleep(estimated_movement_time + 2)  # Wait for estimated movement time + buffer

print("Starting temperature measurements...")

# Acclimatization check
last_temps_therm1 = []
last_temps_therm2 = []

while True:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    temp1, temp2 = td.query_temperatures(thermometers)
    
    data.append([timestamp, aim_height, temp1, temp2])
    
    print(f"Time: {timestamp}, Height: {aim_height}, Temp1: {temp1}, Temp2: {temp2}")
    
    last_temps_therm1.append(temp1)
    last_temps_therm2.append(temp2)
    
    if len(last_temps_therm1) > 20:
        last_temps_therm1.pop(0)
    if len(last_temps_therm2) > 20:
        last_temps_therm2.pop(0)
    
    if len(last_temps_therm1) == 20 and len(last_temps_therm2) == 20:
        max_diff_therm1 = np.max(np.abs(np.diff(last_temps_therm1)))
        max_diff_therm2 = np.max(np.abs(np.diff(last_temps_therm2)))
        
        if max_diff_therm1 < acclimation_tolerance and max_diff_therm2 < acclimation_tolerance:
            print("Both temperatures acclimatized. Experiment complete.")
            break
    
    time.sleep(2)  # Measure every 2 seconds

# Move system back to the top
print("Returning system to the initial height...")
time.sleep(3)
md.send_movement_command(motor, str(initial_height))
md.wait_for_movement_to_complete(motor)

# Close connections
md.close_connection(motor)
td.close_connection(thermometers)

# Save data to a single CSV file
df = pd.DataFrame(data, columns=["Time", "Height", "Temp1 (Ambient)", "Temp2 (Water)"])

timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
df.to_csv(f"temperature_measurements_{timestamp}.csv", index=False)

print("Data saved successfully.")
