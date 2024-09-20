Readme.txt      -> What each File is Doing
Connections.txt -> How Each Component is Connected

Server/appSerial.py        -> Reading the Serial Signals From USB, "Must Check the Connected Port as in here it is COM3"
Server/predict.py          -> Flask Server which Have the Endpoints For Predict and Web View Page
Server/readings.json       -> The Old Readings That The Model Read Before
Server/qt_dataset.csv      -> The Data That We Train the Model On
Server/train.py            -> The Script To Train the Model using Dataset
Server/tiredness_model.pkl -> The Trained Model

ESP32/esp32.ino -> the Hardware Code for ESP32



To Run The Code You Have To Have Some Python Modules:
scikit-learn
Flask
pickle5
pyserial


To Install Each, when You Have pip run the Following Commend on cmd:
pip install {modules Name}

Example:
pip install Flask


To Run the predict.py File using cmd (the Server):
python predict.pY

To Run appSerial.py using cmd:
python appSerial.py 