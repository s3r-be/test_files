#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// rx, tx
SoftwareSerial NodeMCU(D2,D3);

const char* ssid="moto_hotspot";
const char* password = "ggg333444";
String ip = "192.168.0.121";

void setup(){
	
	Serial.begin(9600);
	NodeMCU.begin(4800);
  pinMode(D2,INPUT);
  pinMode(D3,OUTPUT);
  
  Serial.print("Wifi connecting to ");
  Serial.println( ssid );
  // connecting to wifi
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
  Serial.println("");
  Serial.println("Sending Hello message to server " + ip);
  delay(1000);
  int res = sendmessage("Hello");
  delay(1000);
  if (res==1) {
    Serial.println("Send Successfully");
  } else { 
    Serial.println("Error on Server side or client side.");
  }
}


int sendmessage(String d)
{
  int sres;
  int net;
  // send distance data to server.php
  if (WiFi.status()==WL_CONNECTED)
  {
    HTTPClient http;
    String url="http://" + ip + "/ids/server.php?data="+d;
    http.begin(url);
    http.addHeader("Content-Type","text/plain");
    int httpCode=http.GET();
    String payload=http.getString();
    Serial.println("While sending I received this from server : "+payload);
    if (payload=="SUCCESS. Data written in file."){
      sres=1;
    } else {
      sres=0;
      Serial.println("wrong or no payload!");
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


void loop(){
	
	while(NodeMCU.available()>0){
	float val = NodeMCU.parseFloat();
	if(NodeMCU.read()== '\n'){
    Serial.print("revd: ");
	  Serial.println(val);
    int res = sendmessage(String(val));
    if (res==1) {
      Serial.println("Send Successfully");
    } else { 
      Serial.println("Error on Server side or client side.");
    }
	}
}
delay(100);
}
