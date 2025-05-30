# Import necessary libraries and drivers
from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td
import pandas as pd
import numpy as np
import time

# Device connections
motor_port = "COM4"  # Port for Arduino connected to step motor
motor = md.connect_to_arduino(motor_port)  # Create the motor connection

thermometers_port = "COM5"  # Port for thermometers
thermometers = td.connect_to_arduino(thermometers_port)  # Create the thermometers connection

# ----------------------------------------------------------------------------
# Experiment Parameters
initial_height = 1000   # Starting height
distance_to_move = -5   # Step size for each movement
tolerance = 0.3          # Tolerance for acclimatization

# Data storage for all measurements
data = []

# Initialize experiment
current_height = initial_height
md.send_movement_command(motor, str(initial_height))  # Set system to initial height
md.wait_for_movement_to_complete(motor)

md.send_movement_command(motor, str(-130))
md.wait_for_movement_to_complete(motor)

# ----------------------------------------------------------------------------
# Main experiment loop
while current_height > 500:
    print(f"\nStarting measurements at height: {current_height}")

    # Store the last three measurements for acclimatization check
    last_three_temp1 = []
    last_three_temp2 = []

    while True:
        # Read temperatures from the two sensors
        temp1, temp2 = td.query_temperatures(thermometers)  # temp1 = ambient, temp2 = water

        # Record data with timestamp, height, and temperature readings
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data.append([timestamp, current_height, temp1, temp2])
        print(f"Time: {timestamp}, Height: {current_height}, Temp1 (Ambient): {temp1}, Temp2 (Water): {temp2}")

        # Manage the last three measurements for acclimatization check
        last_three_temp1.append(temp1)
        last_three_temp2.append(temp2)

        if len(last_three_temp1) > 3:
            last_three_temp1.pop(0)  # Keep only the last 3 measurements for temp1
        if len(last_three_temp2) > 3:
            last_three_temp2.pop(0)  # Keep only the last 3 measurements for temp2

        # Check acclimatization for both temperatures
        acclimatized_temp1 = False
        acclimatized_temp2 = False

        if len(last_three_temp1) == 3:
            max_diff_temp1 = np.max(np.abs(np.diff(last_three_temp1)))
            acclimatized_temp1 = max_diff_temp1 < tolerance
            if acclimatized_temp1:
                print(f"Temp1 (Ambient) acclimatized with values: {last_three_temp1}")

        if len(last_three_temp2) == 3:
            max_diff_temp2 = np.max(np.abs(np.diff(last_three_temp2)))
            acclimatized_temp2 = max_diff_temp2 < tolerance
            if acclimatized_temp2:
                print(f"Temp2 (Water) acclimatized with values: {last_three_temp2}")

        # If both are acclimatized, move down
        if acclimatized_temp1 and acclimatized_temp2:
            print("System fully acclimatized. Moving down...")
            break

        time.sleep(1)  # Wait 1 second between measurements

    # Move system down for the next measurement phase
    current_height += distance_to_move  # Update the current height
    md.send_movement_command(motor, str(distance_to_move))
    md.wait_for_movement_to_complete(motor)

# ----------------------------------------------------------------------------
# Finish the protocol
print("Experiment completed. Moving system back to the top...")

md.send_movement_command(motor, str(initial_height))  # Move back up
md.wait_for_movement_to_complete(motor)

# Close connections
md.close_connection(motor)
td.close_connection(thermometers)

# ----------------------------------------------------------------------------
# Save data to Excel
df = pd.DataFrame(data, columns=["Time", "Height", "Temp1 (Ambient)", "Temp2 (Water)"])
excel_filename = "temperature_measurements_2.csv"
df.to_csv(excel_filename, index=False)
print(f"Data saved to {excel_filename}")
