import serial
import time
import requests

# Define the URL for sending readings
url = 'http://127.0.0.1:5000/predict'

# Replace 'COMX' with your Bluetooth COM port number
bluetoothCOMPort = 'COM6'

def read_from_bluetooth():
    bluetoothSerial = None
    try:
        # Setup Serial Connection
        bluetoothSerial = serial.Serial(bluetoothCOMPort, baudrate=115200, timeout=1)
        print("Connected to ESP32 via Bluetooth")
        counter = 0
        consistDone = False
        o2Done = False
        BPMDone = False
        while True:
            # try:
                # Read data from ESP32
                data = bluetoothSerial.readline().decode('utf-8').rstrip()
                if data:
                    # print("Received:", data)
                    # print("Consistency" in data)
                    if "Consistency" in data:
                        consist = data.split(" ")
                        consistVal = float(consist[1])
                        consistDone = True
                    elif "Spo2" in data:
                        o2 = data.split(" ")
                        o2Val = float(o2[1])
                        o2Done = True
                    elif "BPM" in data:
                        BPM = data.split(" ")
                        BPMVal = float(BPM[1])
                        BPMDone = True
                    if consistDone and BPMDone and o2Done:
                        print(f"Spo2 {o2Val}, BPM {BPMVal}, Cons {consistVal}")
                        consistDone = False
                        o2Done = False
                        BPMDone = False
                        try:
                            response = requests.get(url+f"?bpm={BPMVal}&o2={o2Val}&sound_rate={consistVal}")
                            print("Res: ",url+f"?bpm={BPMVal}&o2={o2Val}&sound_rate={consistVal}")
                        except:
                            print("Somthing Went Wrong With the Server")
                time.sleep(0.1)
            # except:
                # print("Connecting")

    except serial.SerialException as e:
        print("Error:", e)

    finally:
        if bluetoothSerial:
            bluetoothSerial.close()
            print("Connection closed")

# Run the function
read_from_bluetooth()
