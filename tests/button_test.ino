const int buttonPin = 4;


void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  
  if (buttonState == HIGH) {
    Serial.println("Not Pressed");
  } else {
    Serial.println("Pressed");
  }

  delay(100);
}
