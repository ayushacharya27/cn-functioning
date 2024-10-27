from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, db
import serial
import time
import threading
import json

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate(r"C:\Users\DELL\Desktop\CN_PROJECT\computernetowrk-d0548-firebase-adminsdk-gedtp-dd07cd9ec2.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': r'https://computernetowrk-d0548-default-rtdb.firebaseio.com/'
})

# Reference to the Firebase Realtime Database
ref = db.reference('/sensor')

# Initialize Serial Port
try:
    ser = serial.Serial('COM8', 9600)  # Update 'COM8' if your port is different
    print("Serial port opened successfully.")
except serial.SerialException as e:
    ser = None
    print(f"Failed to open serial port: {e}")

# Function to continuously read serial data and update Firebase
def read_serial_and_update_firebase():
    while True:
        if ser and ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received data: {line}")

            try:
                # Parse the JSON-like string
                data = json.loads(line)

                # Extract values with fallback to zero if None
                Humidity = data.get('humidity', 0)
                Temperature = data.get('temperature', 0)
                Fire = data.get('fire', 0)
                Sound = data.get('sound', 0)
                Distance = data.get('distance', 0)
                Illumination = data.get('light', 0)

                # Optional: Get MPU6050 data if available in JSON
                Accelartion = data.get('Accelartion', 0)
                 
                gyroX = data.get('gyroX', 0)
                gyroY = data.get('gyroY', 0)
                

                # Update Firebase
                ref.set({
                    'Humidity': Humidity,
                    'Temperature': Temperature,
                    'Fire Detection': Fire,
                    'Noise Level': Sound,
                    'Distance From Nearest Object': Distance,
                    'Presence Of Light': Illumination,
                    'Accelerometer':  Accelartion ,
                    'GyroX':   gyroX,
                    'GyroY' : gyroY 

                })

                print(f"Updated Firebase with Humidity: {Humidity}, Temperature: {Temperature}, Fire: {Fire}, "
                      f"Noise Level: {Sound}, Distance: {Distance}, Light: {Illumination}, "
                      f"Accelartion: {Accelartion}, GyroX: {gyroX}, GyroY: {gyroY} ")

            except json.JSONDecodeError as e:
                print(f"Error parsing data: {e}")
            except (KeyError, ValueError) as e:
                print(f"Error extracting values: {e}")

        time.sleep(5)  # Wait for 5 seconds before the next update

# Start the background thread for serial data reading
thread = threading.Thread(target=read_serial_and_update_firebase)
thread.daemon = True
thread.start()

@app.route('/')
def home():
    return jsonify({"message": "Flask server is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
