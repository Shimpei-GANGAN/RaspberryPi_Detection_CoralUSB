#define LED_PIN1 2
byte val = 0;

void setup() {
  pinMode(LED_PIN1, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if ( Serial.available() > 0 ) {
    val = Serial.read();
  }
  //  条件分岐
  if ( val == '1') {
    digitalWrite(LED_PIN1, HIGH);
  }
  else if( val == '0'){
    digitalWrite(LED_PIN1, LOW);
  }
}
