from source.source_voltmeter import Driver_keithley as sv
import numpy as np
import pandas as pd
import time

def current_curve(folder, name, temperature, source, voltmeter, initialC, finalC, nMeasures):
    
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
    data.to_csv(r"{}\measurements_2803LED_{}_{}.csv".format(folder,name,temperature), index=False)
    print("Measurements saved")
    
    
    #----------------------------------------------------------------------------
    
    # Finish the protocol
    
    sv.program_source(source, voltmeter, 0.0, delay,tiempo) # set source at 0.0 amperes
    return