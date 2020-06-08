// Libraries 
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>




const char* ssid="hattarki_2.4";

const char* password = "SH9423570289";



//int ledPin = 13;



void setup() {

  

//  pinMode(ledPin,OUTPUT);

//  digitalWrite(ledPin,LOW);



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



//  digitalWrite( ledPin , HIGH);

  Serial.println();



  Serial.println("Wifi Connected Success!");

  Serial.print("NodeMCU IP Address : ");

  Serial.println(WiFi.localIP() );

  delay(1000);
  Serial.println("");
  Serial.println("Sending message to server espcomm");
  delay(1000);
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

int sendmessage(String d)
{
  int sres;
  int net;
  if (WiFi.status()==WL_CONNECTED)
  {
    HTTPClient http;
    String url="http://192.168.0.101/ids/server.php?data="+d;
    http.begin(url);
    http.addHeader("Content-Type","text/plain");
    int httpCode=http.GET();
    String payload=http.getString();
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

int COUNT = 0;

void loop() {

  // put your main code here, to run repeatedly:
  delay(1000);
  Serial.println("");
  Serial.println("Sending message to server espcomm");
  delay(1000);
  int res=sendmessage("Hello" + String(COUNT++));
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
