// Bluetooth Module
#include "BluetoothSerial.h"

// LCD Libraries
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>

// Heart Rate
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#define REPORTING_PERIOD_MS     1000

// Sound: Define pin numbers
const int analogPin = 4;
const int digitalPin = 2;
const int ledPin = 5;

// Sound: Variables for consistency tracking
float consistency = 0.0;
float downValue = 0.01;
int lowerThreshold;  // The Lower Value That the Sensor is Reading at Steady State
int lowerThresholdCounter = 0;  // Counter To Calculate The Lower Threshold
const int minimumChange = 30;     // The Minimum Absolute Change in Sensor Reading to Detect Noise

// LCD: Initialize the display
Adafruit_PCD8544 display = Adafruit_PCD8544(18, 23, 22, 15, 21);

// Initial Heart Rate Variables
int BPM = 80;
float SpO2 = 96.00;
int counter = 1;
int minimumRate = 110;

// Bluetooth Settings
BluetoothSerial serialBT;

// Heart Rate Sensor Variables
PulseOximeter pox;

uint32_t tsLastReport = 0;

// Callback (registered below) fired when a pulse is detected
void onBeatDetected()
{
    Serial.println("Beat!");
}

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  
  // Bluetooth Initials
  serialBT.begin("ESP32-BT");

  // Set up pin modes For Sound Sensor
  pinMode(ledPin, OUTPUT);
  pinMode(digitalPin, INPUT);
  pinMode(analogPin, INPUT);

  // Initial Display Config
  display.begin();
  display.setContrast(60);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(BLACK);
  display.setCursor(0, 0);
  display.println("Hello");
  display.display();

  //// Heart Rate Initialization 

  // Custom I2C pins for the Heart Rate Sensor
  // Wire.begin(14, 27);

  // Initialize the PulseOximeter instance
  // Failures are generally due to an improper I2C wiring, missing power supply
  // or wrong target chip

  // Custom I2C pins for the Heart Rate Sensor
  Wire.begin(14, 27);

  Serial.print("Initializing pulse oximeter..");
  if (!pox.begin()) {
      Serial.println("FAILED");
      
  } else {
      Serial.println("SUCCESS");

      // Register a callback for the beat detection
      pox.setOnBeatDetectedCallback(onBeatDetected);  
  }





  delay(1000);
}

void loop() {
  
  // Handle Sound Sensor Functionality
  handle_Sound_sensor();

  // Stop The Code While Calculating the lower Sound Threshold
  if (lowerThresholdCounter < 10){
    return;
  }
  
  handle_heart_sensor();

  // Print Values on Serial 
  Serial.print("BPM: ");
  Serial.println(BPM);
  Serial.print("SpO2: ");
  Serial.println(SpO2);

  // Send The Data via Bluetooth Serial
  if (serialBT.connected()) {
    String Spo2DataToSend = "Spo2: " + String(SpO2);
    String BPMDataToSend = "BPM: " + String(BPM);
    serialBT.println(Spo2DataToSend);
    serialBT.println(BPMDataToSend);
  }
  // Play around With the LCD Display
  if (BPM > minimumRate && counter%10 ==0){
    display.clearDisplay();
    display.println("    Shaheeq");
    display.display();
  }else if (BPM > minimumRate && counter%10 == 1){
    display.println("       .");
    display.display();
  }
  else if (BPM > minimumRate && counter%10 == 2){
  display.println("       .");
    display.display();
  }
  else if (BPM > minimumRate && counter%10 == 3){
  display.println("       .");
    display.display();
  
  }
  else if (BPM > minimumRate && counter%10 == 4){
   display.println("");
    display.println("     Zafeer");
    display.display();
  }
  else if (BPM > minimumRate  && counter%10 ==5){
    display.clearDisplay();
    display.println("");
    display.println("");
    display.println(" Ehda Shewaya");
    display.display();
    delay(500);
  }
  else{
    // Clear The Display for Later Prints
    display.clearDisplay();
    display.print("Sound Rt:");// Sount Rate
    display.println(round(consistency));
    display.print("BPM:");
    display.println(BPM);
    display.print("SpO2: ");
    display.println(SpO2);
    display.display();
    counter =-1;
  }

  // Increase The Counter For Next Operation
  counter+=1;
  
  // Delay for a short period
  delay(500);

}

void handle_Sound_sensor(){
  // Read digital and analog values
  float digitalValue = digitalRead(digitalPin);
  float analogValue = analogRead(analogPin);

  // Calculating Lower Threshold
  Serial.print("Thresh Counter: ");
  Serial.println(lowerThresholdCounter);
  Serial.print("Sound:");
  Serial.println(analogValue);
  Serial.print("Sound lowerThreshold:");
  Serial.println(lowerThreshold);
  if (lowerThresholdCounter == 0){
    lowerThreshold=analogValue;
    lowerThresholdCounter+=1;
    display.clearDisplay();
    display.println("Calculating");
    display.println("Sound");
    display.println("Threshold");    display.display();
    delay(500);

  }else if (lowerThresholdCounter < 10){
    lowerThreshold= (analogValue+lowerThreshold) / 2;
    lowerThresholdCounter+=1;
    display.clearDisplay();
    display.println("Calculating");
    display.println("Sound");
    display.println("Threshold");
    display.display();
    delay(500);

  }

  // Calculate absolute change in analog value
  int absChange = abs(lowerThreshold - analogValue);

  // Check conditions for LED activation
  if (digitalValue == HIGH || absChange > minimumChange) {
    consistency += 1.0;
    digitalWrite(ledPin, HIGH);
    // delay(1000);
  } else {
    digitalWrite(ledPin, LOW);

    // Update consistency and downValue
    if (consistency > 0) {
      consistency -= downValue;
      if (downValue < 0.5) {
        downValue += 0.01;
      }
    } else {
      downValue = 0;
      consistency = 0;
    }
  }
  // Send Data Via Bluetooth
  if (serialBT.connected()) {
    String ConsistancyDataToSend = "Consistency: " + String(round(consistency));
    serialBT.println(ConsistancyDataToSend);


  }
  // Print information to the serial monitor
  Serial.print("Digital: ");
  Serial.println(digitalValue);
  Serial.print("Analog: ");
  Serial.println(analogValue);
  Serial.print("absChange: ");
  Serial.println(absChange);
  Serial.print("Consistency: ");
  Serial.println(round(consistency));
}

void handle_heart_sensor(){
  if(pox.begin()){

    // Make sure to call update as fast as possible
    pox.update();

    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        BPM = pox.getHeartRate();
        SpO2 = pox.getSpO2();
        tsLastReport = millis();
    }}
}
