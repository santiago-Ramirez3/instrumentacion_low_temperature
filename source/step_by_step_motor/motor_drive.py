import serial
import time

# - connect_to_arduino works correctly
# - send_movement_command works correctly
# - read_repsonse works correctly
# - wait_for_movement_to_complete works correctly
# - close_connection works correctly
#
# We could define several function to go up or go down until 
# touch the swich, or some function that keep the distance that 
# it has moved
#
# I would like to write this same but using Classes of OOP
# I think the implementation could be better, but this one works.

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

def send_movement_command(arduino, distance_mm):
    """
    Sends the movement command to the Arduino.
    The command format is 'M<distance>' (e.g., 'M100' for 100 mm).
    """
    command = f"M{distance_mm}\n" # command beginning with "M" and distance in mm.
    try:
        arduino.write(command.encode()) # write the command in serial port
        time.sleep(0.2)
        #print(f"Sent command: {command.strip()}") # print the command, but it is not neccesary so far
    except Exception as e:
        print("Error while sending movement command:", e)

def read_response(arduino):
    """
    Reads all available data from the Arduino's serial buffer until a newline ("\n") is encountered.
    Returns the full response as a string or None if no response is available.
    """
    try:
        response = ""
        while arduino.in_waiting > 0:
            response += arduino.read(arduino.in_waiting).decode()
            if "\n" in response:
                break

        response = response.strip()
        if response:
            print(response)
        return response if response else None

    except Exception as e:
        print("Error while reading from Arduino:", e)
        return None


def wait_for_movement_to_complete(arduino):
    """
    Continuously checks for movement completion or interrupts.
    """
    print("Waiting for movement to complete...")
    while True:
        response = read_response(arduino)
        if response:
            if ("Reached top" in response):
                print('Finished by: ',response)
                return response
            if ("Reached bottom" in response):
                print('Finished by: ',response)
                return response # stops waiting when the response is Motor movement complete (may it will be changed for a shorter response)
            elif ("Motor movement complete" in response):
                print('Finished by: ',response)
                return response
        time.sleep(0.1)  # Adjust the polling frequency if needed

def close_connection(arduino):
    """
    Closes the serial connection to the Arduino.
    """
    if arduino:
        arduino.close()
        print("Connection closed.")

# The following is an example function to control the step by step motor
def main():
    port = 'COM4'  # Change this to your Arduino's port (e.g., '/dev/ttyUSB0' on Linux)
    arduino = connect_to_arduino(port)

    if arduino:
        try:
            while True:
                # Get user input for the desired movement distance
                distance = input("Enter distance to move (in mm, positive or negative) or 'q' to quit: ")
                if distance.lower() == 'q':
                    break
                
                try:
                    distance = float(distance)
                    send_movement_command(arduino, distance)
                    wait_for_movement_to_complete(arduino)
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")

        except KeyboardInterrupt:
            print("\nTerminating...")
        finally:
            close_connection(arduino)

def go_down_and_up():
    port = 'COM4'  # Change this to your Arduino's port (e.g., '/dev/ttyUSB0' on Linux)
    arduino = connect_to_arduino(port)

    send_movement_command(arduino, "1000")
    wait_for_movement_to_complete(arduino)
    time.sleep(5)
    send_movement_command(arduino, "-1000")
    wait_for_movement_to_complete(arduino)
    time.sleep(5)
    send_movement_command(arduino, "1000")
    wait_for_movement_to_complete(arduino)

    close_connection(arduino)

if __name__ == '__main__':
    go_down_and_up()
