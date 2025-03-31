# Import file from folders to control the devices
from source_voltmeter import Driver_keithley as sv
from step_by_step_motor import motor_drive as md
from temperature_sensors import thermometers_driver as td

# Import libreries
import pandas as pd
import numpy as np
import time
from simple_pid import PID  # Ensure you have installed the simple_pid library

def current_curve(color, temperature, source, voltmeter, initialC, finalC, nMeasures):
    
    #currents = np.arange(initialC, finalC, setpC) # numerical array with all current value
    currents = np.linspace(initialC, finalC, nMeasures)
    delay = 1
    
    tiempo = time.time() # Obtiene el tiempo actual
    
    print("iniciando toma de datos")
    #----------------------------------------------------------------------------
    
    # Create an empty DataFrame to store the measurements
    columns = ["Current", "Source Measure", "Volt Measure", "Timestamp", "Temperature"]
    data = pd.DataFrame(columns=columns)
    
    for i in currents:
        level = i  # Set the source level
        
        # Program and measure
        source_measure, volt_measure = sv.program_source(source, voltmeter, level, delay, tiempo)
    
        # Capture timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
        # Append the new measurement to the DataFrame
        data = pd.concat([data, pd.DataFrame([[level, source_measure, volt_measure, timestamp, temperature]], columns=columns)], ignore_index=True)
    
        time.sleep(1)
    
    # Save to CSV
    data.to_csv(f"measurements_2803LED_{color}_{temperature}.csv", index=False)
    print("Measurements saved to measurements.csv")
    
    
    #----------------------------------------------------------------------------
    
    # Finish the protocol
    
    sv.program_source(source, voltmeter, 0.0, delay,tiempo) # set source at 0.0 amperes
    return

def reach_temperature(target_temperature, thermometers, motor, color, source, voltmeter, initialC, finalC, nMeasures=10):
    # ----------------------------
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
        while True:
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
                    break
                
            time.sleep(10)  # Measure every 10 seconds
        if  abs(error) < tolerance_temp:
            break
    current_curve(color, target_temperature, source, voltmeter, initialC, finalC, nMeasures)
    return


# ----------------------------
# Device connections
motor_port = "COM14"  # Port for Arduino connected to step motor
motor = md.connect_to_arduino(motor_port)  # Create the motor connection

thermometers_port = "COM13"  # Port for thermometers
thermometers = td.connect_to_arduino(thermometers_port)  # Create the thermometers connection

voltmeter_address = 'GPIB0::22::INSTR' # Voltmeter GPIB address
source_address = 'GPIB0::16::INSTR' # Source GPIB address

source, voltmeter = sv.connect_intruments(source_address, voltmeter_address) # create separated instrument objects

# ----------------------------
# Initialize system position
initial_height = 1000     # Starting (absolute) height
#current_height = initial_height

# Move system to starting position
print("Moving system to initial height...")
md.send_movement_command(motor, str(initial_height))
response = md.wait_for_movement_to_complete(motor)
time.sleep(2)
md.send_movement_command(motor, str("-450"))
response = md.wait_for_movement_to_complete(motor)
time.sleep(10)
# ----------------------------

temperature_list = np.arange(-160,-220,-20)

for temp in temperature_list:
    reach_temperature(target_temperature = temp,
                       thermometers = thermometers,
                       motor = motor,
                       color = "RED_temp1",
                       source = source,
                       voltmeter = voltmeter,
                       initialC = 0.0,
                       finalC = 2.0e-2,
                       nMeasures=10)

# ----------------------------
# Optional: Return system to the starting position
print("PID control loop completed. Returning system to initial height...")
# ----------------------------

md.send_movement_command(motor, "1000") # Get up the system

# close all connections
md.close_connection(motor)
sv.close_instruments(source, voltmeter)
