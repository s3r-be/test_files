// receive ultrasonic data from serial (coming from arduino), send this data to serial and server

// Libraries 
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

int data; //Initialized variable to store recieved data
const char* ssid="moto_hotspot";
const char* password = "ggg333444";
String ip = "192.168.43.121";

void setup() {

  //Serial Begin at 9600 Baud 

  Serial.begin(9600);
  Serial.println();
  Serial.print("Wifi connecting to ");
  Serial.println( ssid );
  WiFi.begin(ssid,password);
  Serial.println();
  Serial.print("Connecting");

  while( WiFi.status() != WL_CONNECTED ){
      delay(500);
      Serial.print(".");        
  }

  Serial.println();
  Serial.println("Wifi Connected Success!");
  Serial.print("NodeMCU IP Address : ");
  Serial.println(WiFi.localIP() );

  delay(1000);
  Serial.println("");
  Serial.println("Sending message to server " + ip);
  delay(1000);
  
//  test message
  int res=sendmessage("Hello");
  delay(1000);
  if (res==1)
  {
    Serial.println("Send Successfully");
  }
  else
  {
    Serial.println("Error on Server side or client side.");
  }
}

// function to send message on server
int sendmessage(String d)
{
  int sres;
  int net;
  if (WiFi.status()==WL_CONNECTED)
  {
    HTTPClient http;
    String url="http://" + ip + "/ids/server.php?data="+d;
    http.begin(url);
    http.addHeader("Content-Type","text/plain");
    int httpCode=http.GET();
    String payload=http.getString();
    Serial.println("url for sending data - " + url);
    Serial.println("While sending I received this from server : "+payload);
    if (payload=="SUCCESS. Data written in file.")
    {
      sres=1;
    }
    else
    {
      sres=0;
    }
    http.end();
    net=1;
  }
  else
  {
    Serial.println("Internet Problem!");
    net=0;
  }
  return (net && sres);
}

void loop() {
  data = -999;

  int bytesAvail = Serial.available();
  Serial.println('bytes available: ' + bytesAvail);
  data = Serial.read(); //Read the serial data and store it
  

// print received data on node mcu serial
//  delay(500);
  Serial.print("rcvd: ");
  Serial.println(data-'0');

// send message to server
//  delay(1000);
  Serial.println("Sending message to server " + ip);
//  delay(1000);
  int res=sendmessage(String(data));
  delay(1000);
  if (res==1)
  {
    Serial.println("Send Successfully");
  }
  else
  {
    Serial.println("Error on Server side or client side.");
  }
  Serial.println("");
}
