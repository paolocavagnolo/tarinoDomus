#include <RFM69.h>         //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>
#include "DHT.h"

#define PIN_a 14  // the pin we are interested in
#define PIN_b 15  // the pin we are interested in
#define PIN_c 16  // the pin we are interested in

#define TRSHLD 50

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

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

#define NODEID      3      // node ID used for this unit
#define NETWORKID   492
#define GATEWAYID   1

#define FREQUENCY   RF69_433MHZ

#define ACK_TIME    30  // # of ms to wait for an ack
#define ENCRYPTKEY "ricercaspiritual" //(16 bytes of your choice - keep the same on all encrypted nodes)

#define LED 9 // Moteinos hsave LEDs on D9

#define DEBOUNCE 70

boolean requestACK = false;

RFM69 radio;


void setup() {
  pinMode(LED, OUTPUT);

  pinMode(PIN_a, INPUT_PULLUP);     
  pinMode(PIN_b, INPUT_PULLUP);     
  pinMode(PIN_c, INPUT_PULLUP);   

  radio.initialize(FREQUENCY, NODEID, NETWORKID);
  radio.encrypt(ENCRYPTKEY); //OPTIONAL

  dht.begin();

  Serial.begin(9600);

}

byte message[3];


bool a_up = false;
bool b_up = false;
bool c_up = false;

long tTemp = 0;
float h = 0;
float t = 0;
char buf[4];

void loop() {

  if (radio.receiveDone()) {
    if (radio.ACKRequested()) radio.sendACK();
  }

  if (millis() - tTemp > 30000) {
    tTemp = millis();
    
    h = dht.readHumidity();
    t = dht.readTemperature();

    dtostrf(t,4,1,buf);
    
    message[0] = 't';
    message[1] = (buf[0]);
    message[2] = (buf[1]);
    message[3] = (buf[3]);
    radio.sendWithRetry(GATEWAYID,message, 4);

    dtostrf(h,4,1,buf);
    
    message[0] = 'h';
    message[1] = (buf[0]);
    message[2] = (buf[1]);
    message[3] = (buf[3]);
    radio.sendWithRetry(GATEWAYID,message, 4);
  }

  //check any button pushed
  if (analogRead(PIN_a) < TRSHLD && !a_up){
    message[0] = 'a';
    message[1] = '1';
    radio.sendWithRetry(GATEWAYID,message, 2);
    a_up = true;
    digitalWrite(LED, HIGH);
    delay(DEBOUNCE);
  }
  if (analogRead(PIN_a) > TRSHLD && a_up){
    message[0] = 'a';
    message[1] = '2';
    radio.sendWithRetry(GATEWAYID,message, 2);
    a_up = false;
    tA++;
    digitalWrite(LED, LOW);
    delay(DEBOUNCE);
  }
  //B
  if (analogRead(PIN_b) < TRSHLD && !b_up){
    message[0] = 'b';
    message[1] = '1';
    radio.sendWithRetry(GATEWAYID,message, 2);
    b_up = true;
    digitalWrite(LED, HIGH);
    delay(DEBOUNCE);
  }
  if (analogRead(PIN_b) > TRSHLD && b_up){
    message[0] = 'b';
    message[1] = '2';
    radio.sendWithRetry(GATEWAYID,message, 2);
    b_up = false;
    tB++;
    digitalWrite(LED, LOW);
    delay(DEBOUNCE);
  }
  //C
  if (analogRead(PIN_c) < TRSHLD && !c_up){
    message[0] = 'c';
    message[1] = '1';
    radio.sendWithRetry(GATEWAYID,message, 2);
    c_up = true;
    digitalWrite(LED, HIGH);
    delay(DEBOUNCE);
  }
  if (analogRead(PIN_c) > TRSHLD && c_up){
    message[0] = 'c';
    message[1] = '2';
    radio.sendWithRetry(GATEWAYID,message, 2);
    c_up = false;
    tC++;
    digitalWrite(LED, LOW);
    delay(DEBOUNCE);
  }

}
