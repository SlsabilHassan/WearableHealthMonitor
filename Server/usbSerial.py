import serial
import time
import requests

# Define the URL for sending readings
url = 'http://127.0.0.1:5000/predict'

# Open serial port (Example: COM3, change to your port)
ser = serial.Serial('COM3', 115200, timeout=1)

# Wait for the serial connection to initialize
time.sleep(2)

try:
    while True:
        if ser.in_waiting > 0:
            # Read the data from the serial port
            data = ser.readline().decode('utf-8').rstrip()
            # Print the data received from the serial port
            # print(data)
            print(data)
            print('--')
            if "Consistency" in data:
                consist = data.split(" ")
                consistVal = float(consist[1])
            elif "SpO2" in data:
                o2 = data.split(" ")
                o2Val = float(o2[1])
            elif "BPM" in data:
                BPM = data.split(" ")
                BPMVal = float(BPM[1])
                try:
                    response = requests.get(url+f"?bpm={BPMVal}&o2={o2Val}&sound_rate={consistVal}")
                    print("Res: ",url+f"?bpm={BPMVal}&o2={o2Val}&sound_rate={consistVal}")
                except:
                    print("Somthing Went Wrong With the Server")
except KeyboardInterrupt:
    print('Interrupted by the user')

except Exception as e:
    print("Error occurred:", str(e))

finally:
    # Close the serial connection
    ser.close()
