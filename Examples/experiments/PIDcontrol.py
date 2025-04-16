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
large_step = -25         # Large step size for initial search
small_step = 10          # Fine adjustment step size for maintaining temperature
tolerance = 0.1          # Tolerance for acclimatization
target_temperature = 0.0 # Target temperature to maintain

# Data storage for all measurements
data = []

# Initialize experiment
current_height = initial_height
md.send_movement_command(motor, str(initial_height))  # Set system to initial height
md.wait_for_movement_to_complete(motor)

searching_for_target = True  # Initially, we are searching for the target temperature

# ----------------------------------------------------------------------------
# Main experiment loop
while True:
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

        # If both are acclimatized, proceed with movement
        if acclimatized_temp1 and acclimatized_temp2:
            print("System fully acclimatized. Evaluating next movement...")

            if searching_for_target:
                # Initial search phase with large steps
                if temp1 > target_temperature or temp2 > target_temperature:
                    print(f"Temperature too high. Moving down by {large_step} units.")
                    md.send_movement_command(motor, str(large_step))
                    current_height += large_step  # large_step is negative

                else:
                    # Switch to fine control mode once the target temperature is reached
                    print("Target temperature reached. Switching to fine control mode.")
                    searching_for_target = False
                md.wait_for_movement_to_complete(motor)
                break

            else:
                # Fine control phase with small steps
                if temp1 > target_temperature or temp2 > target_temperature:
                    print(f"Temperature too high. Moving down by {small_step} units.")
                    md.send_movement_command(motor, str(-small_step))
                    current_height -= small_step

                elif temp1 < target_temperature or temp2 < target_temperature:
                    print(f"Temperature too low. Moving up by {small_step} units.")
                    md.send_movement_command(motor, str(small_step))
                    current_height += small_step

                md.wait_for_movement_to_complete(motor)
                break

        # Check for user input to stop the experiment
        user_input = input("Type 'stop' to end the experiment or press Enter to continue: ")
        if user_input.lower() == "stop":
            print("Experiment stopped by user.")
            break

        time.sleep(1)  # Wait 1 second between measurements

    # Break the main loop if the user wants to stop
    if user_input.lower() == "stop":
        break

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
excel_filename = "temperature_control_experiment.xlsx"
df.to_excel(excel_filename, index=False)
print(f"Data saved to {excel_filename}")
