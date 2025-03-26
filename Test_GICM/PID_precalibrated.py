# Import necessary libraries and drivers
from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td
import pandas as pd
import time
import numpy as np
from simple_pid import PID  # Ensure you have installed the simple_pid library

# ----------------------------
# PID Controller Parameters (using simple_pid)
Kp = 0.43      # Proportional gain
Ki = 0.1      # Integral gain
Kd = 0.01     # Derivative gain

target_temperature = -50.0   # Target water temperature (Temp2) in °C (example setpoint)
tolerance_temp = 0.5          # Acceptable temperature error in 
acclimation_tolerance = 0.5
dt = 20                      # Sampling time (seconds) for each PID cycle
max_iterations = 20       # Maximum number of PID iterations
max_step = 40               # Maximum allowed movement (mm) per iteration

# Create a PID object with the target temperature as the setpoint
pid = PID(Kp, Ki, Kd, setpoint=target_temperature)
pid.sample_time = dt
pid.output_limits = (-max_step, max_step)  # Limit the PID output to avoid excessive movements

# ----------------------------
# Device connections
motor_port = "COM14"  # Port for Arduino connected to step motor
motor = md.connect_to_arduino(motor_port)  # Create the motor connection

thermometers_port = "COM13"  # Port for thermometers
thermometers = td.connect_to_arduino(thermometers_port)  # Create the thermometers connection

# ----------------------------
# Initialize system position
initial_height = 1000     # Starting (absolute) height
current_height = initial_height

# Move system to starting position
print("Moving system to initial height...")
md.send_movement_command(motor, str(initial_height))
response = md.wait_for_movement_to_complete(motor)
time.sleep(2)
md.send_movement_command(motor, str("-160"))
response = md.wait_for_movement_to_complete(motor)
time.sleep(5)
# ----------------------------
# Prepare for PID control loop
data = []  # Data storage for logging measurements
iteration = 0
consecutive_within_tolerance = 0
required_consecutive = 5  # Number of consecutive cycles within tolerance to declare stability

print("Starting PID control loop to reach target temperature using simple_pid...")

while iteration < max_iterations:
    iteration += 1

    # Read temperatures from the sensors
    temp1, temp2 = td.query_temperatures(thermometers)
    measured_temp = temp2  # Using water temperature (Temp2) for control
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Compute the movement command using the PID controller
    movement = pid(measured_temp)
    error = target_temperature - measured_temp

    # Log the current measurement and PID output
    data.append([timestamp, current_height, measured_temp, error, movement])
    print(f"{timestamp} | Height: {current_height} | Temp: {measured_temp}°C | Error: {error:.2f} | Movement Command: {movement:.2f}")

    # Avoid commanding a very small movement that might not overcome system inertia
    if abs(movement) < 0.5:
        movement = 0

    if movement != 0:
        print(f"Sending movement command: {movement:.2f}")
        md.send_movement_command(motor, str(movement))
        response = md.wait_for_movement_to_complete(motor)
        print(f"Motor response: {response}")
        current_height += movement  # Update current height based on relative movement
    else:
        print("No significant movement commanded this cycle.")

    # Wait for dt seconds before the next cycle to allow the system to stabilize
    #time.sleep(dt)
    # Acclimatization check
    last_temps_therm1 = []
    last_temps_therm2 = []
    while True:
        temp1, temp2 = td.query_temperatures(thermometers)
        
        data.append([timestamp, temp1, temp2])
        
        print(f"Time: {timestamp}, Temp1: {temp1}, Temp2: {temp2}")
        
        #last_temps_therm1.append(temp1)
        last_temps_therm2.append(temp2)
        
        #if len(last_temps_therm1) > 20:
        #    last_temps_therm1.pop(0)
        if len(last_temps_therm2) > 5:
            last_temps_therm2.pop(0)
        
        #if len(last_temps_therm1) == 20 and len(last_temps_therm2) == 20:
        if len(last_temps_therm2) == 5:
           # max_diff_therm1 = np.max(np.abs(np.diff(last_temps_therm1)))
            max_diff_therm2 = np.max(np.abs(np.diff(last_temps_therm2)))
            print(max_diff_therm2)
            
            if max_diff_therm2 < acclimation_tolerance:
                print("temperature acclimatized. Experiment complete.")
                break
        
        time.sleep(3)  # Measure every 2 seconds    

# ----------------------------
# Optional: Return system to the starting position
print("PID control loop completed. Returning system to initial height...")
height_difference = initial_height - current_height
if height_difference != 0:
    md.send_movement_command(motor, str(height_difference))
    md.wait_for_movement_to_complete(motor)
    print(f"System moved by {height_difference} to reach the initial height.")

# Close connections
md.close_connection(motor)
td.close_connection(thermometers)

# ----------------------------
# Save the collected data to a CSV file
df = pd.DataFrame(data, columns=["Time", "Height", "Measured Temp (Water)", "Error", "PID Output"])
excel_filename = "PID_data\pid_control_library_data_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ".csv"
df.to_csv(excel_filename, index=False)
print(f"Data saved to {excel_filename}")
