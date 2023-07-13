#include <Wire.h>
#include "Adafruit_AS726x.h"

//crear el objeto
Adafruit_AS726x ams;

// búfer para contener valores sin procesar
uint16_t sensorValues[AS726x_NUM_CHANNELS];

//búfer para almacenar valores calibrados (no se usa de forma predeterminada en este ejemplo)
float calibratedValues[AS726x_NUM_CHANNELS];

void setup() {
  Serial.begin(9600);
  while(!Serial);
  
// inicializa el pin digital LED_BUILTIN como salida.
  pinMode(LED_BUILTIN, OUTPUT);

  //empezar y asegurarnos de que podamos conectar con el sensor
  if(!ams.begin()){
    Serial.println("could not connect to sensor! Please check your wiring.");
    while(1);
  }
}

void loop() {

  uint8_t temp = ams.readTemperature();
  float violet = -log10(calibratedValues[AS726x_VIOLET]/34000.00);
  float blue = -log10(calibratedValues[AS726x_BLUE]/37000.00);
  float green = -log10(calibratedValues[AS726x_GREEN]/15000.00);
  float yellow = -log10(calibratedValues[AS726x_YELLOW]/37000.00);
  float orange = -log10(calibratedValues[AS726x_ORANGE]/2400.00);
  float red = -log10(calibratedValues[AS726x_RED]/7500.00);
  
  ams.startMeasurement(); //comenzar una medicion
  
  //espera hasta que los datos estén disponibles
  bool rdy = false;
  while(!rdy){
    delay(5);
    rdy = ams.dataReady();
  }

  ams.readRawValues(sensorValues);
  ams.readCalibratedValues(calibratedValues);

    Serial.print("350"); Serial.print(","); Serial.println("0");
    Serial.print("400"); Serial.print(","); Serial.println("0");
    Serial.print("450"); Serial.print(","); Serial.println(violet);
    Serial.print("500"); Serial.print(","); Serial.println(blue);
    Serial.print("550"); Serial.print(","); Serial.println(green);
    Serial.print("570"); Serial.print(","); Serial.println(yellow);
    Serial.print("600"); Serial.print(","); Serial.println(orange);
    Serial.print("650"); Serial.print(","); Serial.println(red);
    Serial.print("700"); Serial.print(","); Serial.println("0");
    Serial.print("750"); Serial.print(","); Serial.println("0");
 
  delay(1000);
}
