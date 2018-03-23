#include <RFM69.h>         //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>

#define Reset_AVR() wdt_enable(WDTO_30MS); while(1) {}

#define NODEID      12      // node ID used for this unit
#define NETWORKID   492
#define GATEWAYID   1

#define FREQUENCY   RF69_433MHZ

#define ACK_TIME    30  // # of ms to wait for an ack
#define ENCRYPTKEY "ricercaspiritual" //(16 bytes of your choice - keep the same on all encrypted nodes)

// 1: GATEWAY
// 2: ingresso
// 3: ingresso > antibagno
// 4: antibagno > ingresso
// 5: antibagno > bagno
// 6: bagno
// 7: letto > antibagno
// 8: letto > cabina
// 9: cabina > letto
// 10: letto
// 11: cucina
// 20: caldaia

#define LED 20 // Moteinos hsave LEDs on D9

boolean requestACK = false;

RFM69 radio;

void setup() {
  pinMode(LED, OUTPUT);

  pinMode(7, OUTPUT);     //set the pin to input

  radio.initialize(FREQUENCY, NODEID, NETWORKID);
  radio.encrypt(ENCRYPTKEY); //OPTIONAL
}


void loop() {

  if (radio.receiveDone()) {
    if (radio.DATA[0] == 100) {
      digitalWrite(7, HIGH);
    }
    else if (radio.DATA[0] == 90) {
      digitalWrite(7, LOW);
    }
    if (radio.ACKRequested()) radio.sendACK();
  }

}