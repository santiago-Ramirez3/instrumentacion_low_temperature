from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td

from simple_pid import PID  # Ensure you have installed the simple_pid library
import numpy as np
import time

def reach_temperature_PID(target_temperature, thermometers, motor):
    # ------------------------------------------------------------------------------------
    # PID Controller Parameters (using simple_pid)
    Kp = 0.3      # Proportional gain
    Ki = 0.0      # Integral gain
    Kd = 0.0     # Derivative gain

    tolerance_temp = 5         # Acceptable temperature error in 
    acclimation_tolerance = 0.5
    dt = 20                      # Sampling time (seconds) for each PID cycle
    max_iterations = 150       # Maximum number of PID iterations
    max_step = 25              # Maximum allowed movement (mm) per iteration

    # Create a PID object with the target temperature as the setpoint
    pid = PID(Kp, Ki, Kd, setpoint=target_temperature)
    pid.sample_time = dt
    pid.output_limits = (-max_step, max_step)  # Limit the PID output to avoid excessive movements

    print("Starting PID control loop to reach target temperature using simple_pid...")
    iteration = 0
    while iteration < max_iterations:
        iteration += 1

        # Read temperatures from the sensors
        temp1, temp2 = td.query_temperatures(thermometers)
        measured_temp = temp1  # Using water temperature (Temp2) for control
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Compute the movement command using the PID controller
        movement = pid(measured_temp)
        error = target_temperature - measured_temp

        # Log the current measurement and PID output
        #data.append([timestamp, current_height, measured_temp, error, movement])
        print(f"{timestamp} | Temp: {measured_temp}°C | Error: {error:.2f} | Movement Command: {movement:.2f}")

        # Avoid commanding a very small movement that might not overcome system inertia
        if abs(movement) < 0.5:
            movement = 0

        if movement != 0:
            print(f"Sending movement command: {movement:.2f}")
            md.send_movement_command(motor, str(movement))
            response = md.wait_for_movement_to_complete(motor)
            print(f"Motor response: {response}")
            #current_height += movement  # Update current height based on relative movement
        else:
            print("No significant movement commanded this cycle.")

        # Wait for dt seconds before the next cycle to allow the system to stabilize
        #time.sleep(dt)
        # Acclimatization check
        last_temps_therm1 = []
        last_temps_therm2 = []

        tolerance_temperature_reached = False

        while not(tolerance_temperature_reached):
            temp1, temp2 = td.query_temperatures(thermometers)

            #data.append([timestamp, temp1, temp2])

            print(f"Time: {timestamp}, Temp1: {temp1}, Temp2: {temp2}")

            #last_temps_therm1.append(temp1)
            last_temps_therm1.append(temp1)

            #if len(last_temps_therm1) > 20:
            #    last_temps_therm1.pop(0)
            if len(last_temps_therm1) > 8:
                last_temps_therm1.pop(0)

            #if len(last_temps_therm1) == 20 and len(last_temps_therm2) == 20:
            if len(last_temps_therm1) == 8:
               # max_diff_therm1 = np.max(np.abs(np.diff(last_temps_therm1)))
                max_diff_therm1 = np.max(np.abs(np.diff(last_temps_therm1)))
                print(max_diff_therm1)

                if (max_diff_therm1 < acclimation_tolerance):
                    print("temperature acclimatized. Experiment complete.")
                    tolerance_temperature_reached = True
                
            time.sleep(10)  # Measure every 10 seconds
        if  abs(error) < tolerance_temp:
            return