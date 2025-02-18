import pyvisa
import time

def control_power_supply(ps, level, delay=1):
    """
    Controls the power supply by sending a series of SCPI commands to:
      - Set remote mode.
      - Configure it for DC output.
      - Set the desired output level.
    """
    ps.write("REMOTE716")        # Set remote control mode
    ps.write("F1,0X")            # Configure for DC output (first command)
    ps.write("F1,0X")            # Configure for DC output (repeat as required)
    ps.write(f"B'{level}',0,0X")  # Set the output level
    ps.write("L100,0X")          # Configure load parameters
    ps.write("R1X")              # Enable trigger input
    ps.write("N1X")              # Switch instrument to operate state
    ps.write("H0X")              # Send trigger signal
    ps.write("G1,2,0X")          # Set communication format
    time.sleep(delay)            # Allow time for the device to stabilize

def read_voltimeter(vm):
    """
    Reads the measurement from the voltmeter using a SCPI query.
    (The command *IDN? is used here as a placeholder. Adjust it to the actual
    measurement command if needed.)
    """
    response = vm.query("*IDN?")
    try:
        value = float(response)
    except ValueError:
        value = response.strip()
    return value

def main():
    # Create a PyVISA resource manager
    rm = pyvisa.ResourceManager()

    # Define the GPIB addresses for the power supply and voltmeter
    power_supply_address = 'GPIB0::16::INSTR'
    voltimeter_address = 'GPIB0::22::INSTR'

    # Open communication with the instruments
    ps = rm.open_resource(power_supply_address)
    vm = rm.open_resource(voltimeter_address)

    # Optionally configure the voltmeter (adjust commands as necessary)
    vm.write("F10STX")
    vm.write("10NX")

    # Set the desired power supply output level (modify the level as needed)
    level = 1.0 * 10 
    control_power_supply(ps, level)

    # Read and display the voltmeter measurement
    volt_value = read_voltimeter(vm)
    print("Voltimeter reading:", volt_value)

    # Close the communications with the instruments
    vm.close()
    ps.close()

if __name__ == "__main__":
    main()
