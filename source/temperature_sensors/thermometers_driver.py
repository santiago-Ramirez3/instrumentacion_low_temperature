import serial
import time

# - connect_to_arduino works correctly
# - query_temperatures works correctly
# - close_connection works correctly
#
# It is a simple code only for connecting, reading, and close both thermometers

def connect_to_arduino(port, baud_rate=115200, timeout=2):
    """
    Establishes connection to the Arduino.
    """
    try:
        arduino = serial.Serial(port, baud_rate, timeout=timeout)
        time.sleep(2)  # Wait for the connection to be established
        print("Connected to Arduino on port:", port)
        return arduino
    except serial.SerialException:
        print("Failed to connect to Arduino. Check the port and try again.")
        return None

def query_temperatures(arduino):
    """
    Queries the Arduino for temperature readings.
    """
    try:
        arduino.write(b'T')  # Send request for temperatures
        response = arduino.readline().decode().strip()
        if response:
            temperature1, temperature2 = response.split(';')
            return float(temperature1), float(temperature2)
        else:
            print("No response from Arduino.")
            return None, None
    except Exception as e:
        print("Error while querying temperatures:", e)
        return None, None

def close_connection(arduino):
    """
    Closes the serial connection to the Arduino.
    """
    if arduino:
        arduino.close()
        print("Connection closed.")

# The following is an example function to read both thermometers
def main():
    port = 'COM5'  # Change this to your Arduino's port (e.g., '/dev/ttyUSB0' on Linux)
    arduino = connect_to_arduino(port)

    if arduino:
        try:
            while True:
                temp1, temp2 = query_temperatures(arduino)
                if temp1 is not None and temp2 is not None:
                    print(f"Temperature 1: {temp1} °C, Temperature 2: {temp2} °C")
                time.sleep(2)  # Adjust query frequency as needed
        except KeyboardInterrupt:
            print("\nTerminating...")
        finally:
            close_connection(arduino)

if __name__ == '__main__':
    main()
