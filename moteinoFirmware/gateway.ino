#include <RFM69.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>//get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>      //comes with Arduino IDE (www.arduino.cc)
#include <SPIFlash.h> //get it here: https://www.github.com/lowpowerlab/spiflash

//*********************************************************************************************
//************ IMPORTANT SETTINGS *************************************************************
//*********************************************************************************************
#define GATEWAYID     1
#define NETWORKID     492  //the same on all nodes that talk to each other
//Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#define FREQUENCY     RF69_433MHZ
#define ENCRYPTKEY    "ricercaspiritual" //exactly the same 16 characters/bytes on all nodes!
#define SERIAL_BAUD   115200
//pinout
#define LED           9 // Moteinos have LEDs on D9
//*********************************************************************************************

uint32_t packetCount = 0;

RFM69 radio;

void setup() {

  Serial.begin(SERIAL_BAUD);
  delay(10);
  radio.initialize(FREQUENCY,GATEWAYID,NETWORKID);

  radio.encrypt(ENCRYPTKEY);

}

int idNode;
byte state;

void loop() {
  if (radio.receiveDone())
  {
    Serial.print('<');
    Serial.print(',');
    Serial.print(packetCount++);
    Serial.print(',');
    Serial.print(radio.SENDERID,DEC);
    Serial.print(',');
    Serial.print(1);
    Serial.print(',');
    Serial.print(radio.RSSI);
    for (byte i = 0; i < radio.DATALEN; i++) {
      Serial.print(',');
      Serial.print(radio.DATA[i],HEX);
    }
    Serial.print(',');
    Serial.println('>');
    //Check
    if (radio.ACKRequested()) radio.sendACK();
  }

  if (Serial.available() > 0)
  {
     String message = Serial.readString();
     if (message[0] == 'R') {
       message.remove(0,1);
       state = message.toInt();
       radio.sendWithRetry(20, state, 1);
     }
     
  }

}