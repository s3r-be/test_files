#include <SoftwareSerial.h>

// rx, tx
SoftwareSerial ArduinoUno(3,2);

// defines pins numbers
const int trigPin = 9;
const int echoPin = 10;

// defines variables
long duration;
int distance;

void setup(){
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
	Serial.begin(9600);
 ArduinoUno.begin(4800);
	
	
}

void loop(){
//	int i = 10;
 // Clears the trigPin
digitalWrite(trigPin, LOW);
delayMicroseconds(2);

// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);

// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);

// Calculating the distance
distance= duration*0.034/2;
ArduinoUno.print(distance);
ArduinoUno.println("\n");
Serial.println(distance);
delay(100);
}
