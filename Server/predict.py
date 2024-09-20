from flask import Flask, request, jsonify,render_template
import pickle
import json

app = Flask(__name__)

# Load The model here
model_path = "tiredness_model.pkl"
with open(model_path, 'rb') as file:
    model = pickle.load(file)

data_file_path = "readings.json"


@app.route("/")
def Hello():
    return jsonify("Hello From Server Side")


@app.route('/predict')
def predict():
    data = request.args
    heart_rate = float(data['bpm'])
    o2_level = float(data['o2'])
    sound_rate = float(data['sound_rate'])  # Assuming 'sound_rate' is a float

    # Prepare the data for the model
    input_data = [heart_rate, o2_level]
    prediction = model.predict([input_data])[0]
    print("predict = ",prediction)
    # Save the data
    status  = ''
    
    # Adding Some Logic Predictions
    # if heart_rate >110:
    #     status = "Check Your Son"
    # elif prediction == 0:
    #     status =  "Your Son's Health is Good"
    

    if heart_rate < 75:
        status =  "Your son's Heart Rate and O2 level are Low \nPossibilities: bradycardia, hypoxemia"
    elif heart_rate > 110:
        status = status + "Your son's Heart Rate is High \nPossibilities: Anxiety, tachycardia"
    else:
        status = "Your Son's Health is Good"

    last10Check = get_last_10()
    if last10Check==1:
        if prediction == 0:
            status =   "Your son's Last 10 Readings Have More Than 5 Low,\nYour Son's Might Not Wearing the Watch"
        else:
            status =   "Your son's Last 10 Readings Have More Than 5 Low,\nYour Son's Might Not Wearing the Watch\n"+status
    save_reading({'heart_rate': heart_rate, 'o2_level': o2_level, 'sound_rate': sound_rate,'message':status})
    return jsonify(status)

@app.route("/lastReadings")
def lastRead():
    # Read existing data
    try:
        with open(data_file_path, 'r') as file:
            readings = json.load(file)
    except FileNotFoundError:
        readings = []

    # Check if the last 10 readings have a heart rate lower than 70
    last_one = readings[-1]
    return last_one
    
@app.route("/view")
def viewHTML():
 return render_template('index.html')


def save_reading(reading):
    # Read existing data
    try:
        with open(data_file_path, 'r') as file:
            readings = json.load(file)
    except FileNotFoundError:
        readings = []

    # Add new reading
    readings.append(reading)

    # Save the updated data
    with open(data_file_path, 'w') as file:
        json.dump(readings, file)


def get_last_10():
    # Read existing data
    try:
        with open(data_file_path, 'r') as file:
            readings = json.load(file)
    except FileNotFoundError:
        readings = []

    # Check if the last 10 readings have a heart rate lower than 70
    last_10_readings = readings[-10:]
    low_heart_rate_count = sum(1 for reading in last_10_readings if reading.get('heart_rate', 0) < 70)

    if low_heart_rate_count >= 5:
        return 1
    else:
        return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
