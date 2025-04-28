
import serial  # Import required libraries
import json  # Import required libraries
import time  # Import required libraries

# Configure your serial port
SERIAL_PORT = '/dev/ttyUSB0'  # Change if you use another port  # Define the serial port to listen to
BAUD_RATE = 115200  # Define the baud rate for serial communication

def procesar_datos(data):  # Function to process incoming JSON data from serial port
    try:
        lectura = json.loads(data)  # Parse the JSON-formatted data string
        print("Data received:")  # Print parsed sensor values
        print(f"ET: {lectura['ET']} °C")  # Print parsed sensor values
        print(f"RH: {lectura['RH']} %")
        print(f"HT: {lectura['HT']} °C")
        print(f"HH: {lectura['HH']} %")
        print(f"WS: {lectura['WS']} km/h")
        return lectura  # Return parsed sensor data as dictionary
    except json.JSONDecodeError:  # Handle invalid JSON format errors
        print("Invalid format:", data)
        return None

def escuchar_serial():  # Function to continuously listen to the serial port
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:  # Open the serial port with specified settings
            print(f"Waiting for data in {SERIAL_PORT} @ {BAUD_RATE} baud...")
            while True:  # Continuously read lines from the serial connection
                linea = ser.readline().decode('utf-8').strip()  # Read and decode one line from the serial port
                if linea:  # If line is not empty, process it
                    procesar_datos(linea)
                time.sleep(0.5)  # Wait briefly between reads
    except serial.SerialException as e:  # Handle serial connection errors
        print("Serial connection error:", e)

if __name__ == "__main__":  # Main program entry point
    escuchar_serial()  # Start listening to serial port
