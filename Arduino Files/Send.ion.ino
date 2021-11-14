//Send.ino

#include<SPI.h>
#include<RF24.h>
#include<String.h>
// ce, csn pins
RF24 radio(9, 10);
int val;
int tempPin = 2;
void setup(void){
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x64);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
  Serial.begin(9600);

}

void loop(void){
  char text[10];
  val = analogRead(tempPin);
  float mv = ( val/1024.0)*5000; 
  float cel = mv/10;
  //float farh = (cel*9)/5 + 32;
 // Serial.println(cel);
  dtostrf(cel, 5, 2, text); 
  //text[6]="2";
  Serial.println(text);
  radio.write(&text, sizeof(text));
 
  delay(1000);

}
