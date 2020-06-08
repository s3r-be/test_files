#include<SoftwareSerial.h> //Included SoftwareSerial Library

//Started SoftwareSerial at RX and TX pin of arduino

SoftwareSerial s(0,1);



void setup() {

  //Serial S Begin at 9600 Baud

  s.begin(9600);

}



void loop() {

  //Write '123' to Serial

  s.write(123);

  delay(1000);

}
