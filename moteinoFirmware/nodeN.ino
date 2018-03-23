#include <RFM69.h>         //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>

#define PIN_a 14  // the pin we are interested in
#define PIN_b 15  // the pin we are interested in
#define PIN_c 16  // the pin we are interested in
volatile byte tA = 0;  // a counter to see how many times the pin has changed
volatile byte tB = 0;  // a counter to see how many times the pin has changed
volatile byte tC = 0;  // a counter to see how many times the pin has changed

#define Reset_AVR() wdt_enable(WDTO_30MS); while(1) {}

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

#define NODEID      9      // node ID used for this unit
#define NETWORKID   492
#define GATEWAYID   1

#define FREQUENCY   RF69_433MHZ

#define ACK_TIME    30  // # of ms to wait for an ack
#define ENCRYPTKEY "ricercaspiritual" //(16 bytes of your choice - keep the same on all encrypted nodes)

#define LED 9 // Moteinos hsave LEDs on D9

boolean requestACK = false;

RFM69 radio;

void setup() {
  pinMode(LED, OUTPUT);

  pinMode(PIN_a, INPUT);     //set the pin to input
  digitalWrite(PIN_a, HIGH); //use the internal pullup resistor
  pinMode(PIN_b, INPUT);     //set the pin to input
  digitalWrite(PIN_b, HIGH); //use the internal pullup resistor
  pinMode(PIN_c, INPUT);     //set the pin to input
  digitalWrite(PIN_c, HIGH); //use the internal pullup resistor

  radio.initialize(FREQUENCY, NODEID, NETWORKID);
  radio.encrypt(ENCRYPTKEY); //OPTIONAL
}

byte message[3];


bool a_up = false;
bool b_up = false;
bool c_up = false;

void loop() {

  if (radio.receiveDone()) {
    if (radio.ACKRequested()) radio.sendACK();
  }


  //check any button pushed
  if (!digitalRead(PIN_a) && !a_up){
    message[0] = 'a';
    message[1] = '1';
    radio.sendWithRetry(GATEWAYID,message, 2);
    a_up = true;
    digitalWrite(LED, HIGH);
    delay(50);
  }
  if (digitalRead(PIN_a) && a_up){
    message[0] = 'a';
    message[1] = '2';
    radio.sendWithRetry(GATEWAYID,message, 2);
    a_up = false;
    tA++;
    digitalWrite(LED, LOW);
  }
  //B
  if (!digitalRead(PIN_b) && !b_up){
    message[0] = 'b';
    message[1] = '1';
    radio.sendWithRetry(GATEWAYID,message, 2);
    b_up = true;
    digitalWrite(LED, HIGH);
    delay(50);
  }
  if (digitalRead(PIN_b) && b_up){
    message[0] = 'b';
    message[1] = '2';
    radio.sendWithRetry(GATEWAYID,message, 2);
    b_up = false;
    tB++;
    digitalWrite(LED, LOW);
  }
  //C
  if (!digitalRead(PIN_c) && !c_up){
    message[0] = 'c';
    message[1] = '1';
    radio.sendWithRetry(GATEWAYID,message, 2);
    c_up = true;
    digitalWrite(LED, HIGH);
    delay(50);
  }
  if (digitalRead(PIN_c) && c_up){
    message[0] = 'c';
    message[1] = '2';
    radio.sendWithRetry(GATEWAYID,message, 2);
    c_up = false;
    tC++;
    digitalWrite(LED, LOW);
  }

}