
import serial
import json
import time

# Configure your serial port
SERIAL_PORT = '/dev/ttyUSB0'  # Change if you use another port
BAUD_RATE = 115200

def procesar_datos(data):
    try:
        lectura = json.loads(data)
        print("Data received:")
        print(f"ET: {lectura['ET']} °C")
        print(f"RH: {lectura['RH']} %")
        print(f"HT: {lectura['HT']} °C")
        print(f"HH: {lectura['HH']} %")
        print(f"WS: {lectura['WS']} km/h")
        return lectura
    except json.JSONDecodeError:
        print("Invalid format:", data)
        return None

def escuchar_serial():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            print(f"Waiting for data in {SERIAL_PORT} @ {BAUD_RATE} baud...")
            while True:
                linea = ser.readline().decode('utf-8').strip()
                if linea:
                    procesar_datos(linea)
                time.sleep(0.5)
    except serial.SerialException as e:
        print("Serial connection error:", e)

if __name__ == "__main__":
    escuchar_serial()
