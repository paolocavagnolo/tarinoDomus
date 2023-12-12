#include <FastLED.h>
#define NUM_LEDS 145
#define DATA_PIN 5

#define PIN_a 14  // the pin we are interested in
#define PIN_b 15  // the pin we are interested in
#define PIN_c 16  // the pin we are interested in

#define TRSHLD 50

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

#define LED 9 // Moteinos hsave LEDs on D9

CRGB leds[NUM_LEDS];

void setup() {
  pinMode(LED, OUTPUT);

  pinMode(PIN_a, INPUT_PULLUP);
  pinMode(PIN_b, INPUT_PULLUP);
  pinMode(PIN_c, INPUT_PULLUP);

  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);  // GRB ordering is typical

  FastLED.setTemperature(Candle);
  FastLED.setBrightness(0);

  for (uint8_t ll = 0; ll < NUM_LEDS; ll++) {
    leds[ll] = CRGB(255, 140, 100);
  }
  FastLED.show();

}

byte message[3];


bool a_up = false;
bool b_up = false;
bool c_up = false;

unsigned long timeAS = 0;
bool lightState = false;
bool pLed = true;

unsigned long delta = 0;

int bri = 0;
int idx = 0;

unsigned long ts = 0;

bool rampUp = false;
bool rampDown = false;

bool cc = false;

void loop() {

  if (cc) {
    cc = false;
    FastLED.setBrightness(dim8_lin(bri));
    FastLED.show();
  }

  if (rampUp) {

    if ((millis() - ts) > 20) {
      ts = millis();
      cc = true;
      bri=bri+1;
    }

    if (bri >= 200) {
      bri = 200;
      rampUp = false;
    }
  }

  if (rampDown) {

    if ((millis() - ts) > 20) {
      ts = millis();
      cc = true;
      bri=bri-1;
    }

    if (bri <= 0) {
      bri = 0;
      rampDown = false;
    }
  }

  if (pLed) {
  
    if (lightState) {
      lightState = false;
      //bri = 0;
      rampUp = true;
      rampDown = false;
    }
    else {
      lightState = true;
      //bri = 200;
      rampDown = true;
      rampUp = false;
    }
    pLed = false;
  }


  //B
  if (analogRead(PIN_b) < TRSHLD && !b_up) {
    b_up = true;
    timeAS = millis();
    digitalWrite(LED, HIGH);
    delay(150);
  }
  if (analogRead(PIN_b) > TRSHLD && b_up) {
    b_up = false;
    pLed = true;
    idx = 0;
    tB++;
    digitalWrite(LED, LOW);
    delay(150);
  }


}
