#include <Wire.h>
#include "Adafruit_AS726x.h"

//create the object
Adafruit_AS726x ams;

//buffer to hold raw values
uint16_t sensorValues[AS726x_NUM_CHANNELS];

//buffer to hold calibrated values (not used by default in this example)
float calibratedValues[AS726x_NUM_CHANNELS];

void setup() {
  Serial.begin(9600);
  while(!Serial);
  
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  //begin and make sure we can talk to the sensor
  if(!ams.begin()){
    Serial.println("could not connect to sensor! Please check your wiring.");
    while(1);
  }
}

void loop() {

  //read the device temperature
  // Se normaliza con respecto a 35000 porque este es el máximo que llega el LED
  uint8_t temp = ams.readTemperature();
  float violet = calibratedValues[AS726x_VIOLET];
  float blue = calibratedValues[AS726x_BLUE];
  float green = calibratedValues[AS726x_GREEN];
  float yellow = calibratedValues[AS726x_YELLOW];
  float orange = calibratedValues[AS726x_ORANGE];
  float red = calibratedValues[AS726x_RED];
  
  //ams.drvOn(); //uncomment this if you want to use the driver LED for readings
  ams.startMeasurement(); //begin a measurement
  
  //wait till data is available
  bool rdy = false;
  while(!rdy){
    delay(5);
    rdy = ams.dataReady();
  }
  //ams.drvOff(); //uncomment this if you want to use the driver LED for readings

  //read the values!
  ams.readRawValues(sensorValues);
  ams.readCalibratedValues(calibratedValues);
  

  //Serial.print("Temp: "); Serial.print(temp);
  //Nm vs Intensity (a.u)
    Serial.print("450"); Serial.print(","); Serial.println(violet);
    Serial.print("500"); Serial.print(","); Serial.println(blue);
    Serial.print("550"); Serial.print(","); Serial.println(green);
    Serial.print("570"); Serial.print(","); Serial.println(yellow);
    Serial.print("600"); Serial.print(","); Serial.println(orange);
    Serial.print("650"); Serial.print(","); Serial.println(red);
 
  delay(1000);
}
