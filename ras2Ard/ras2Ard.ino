#define LED_PIN1 2
//byte val = 0;

void setup() {
  pinMode(LED_PIN1, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  String str;
  if ( Serial.available() > 0 ) {
    str = Serial.readStringUntil(';');
    //  条件分岐
    if(str == "1"){
      digitalWrite(LED_PIN1, HIGH);
      Serial.println(str);
      //Serial.write(str);
    }
    else if( str == "0"){
      digitalWrite(LED_PIN1, LOW);
      Serial.println(str);
    }
    else{
      Serial.println("Enter the correct command.");
    }
  }
}
