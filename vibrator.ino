int vibPin = 5;   // Vibrator connected to GPIO5

void setup() {
  pinMode(vibPin, OUTPUT);
  digitalWrite(vibPin, LOW);  // make sure it's off at start
}

void loop() {
  // Turn vibrator ON for 1 second
  digitalWrite(vibPin, HIGH);
  delay(1000);

  // Turn vibrator OFF for 1 second
  digitalWrite(vibPin, LOW);
  delay(1000);
}
