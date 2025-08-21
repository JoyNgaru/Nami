int buttonPin = 4;   // Button input pin
int vibPin    = 5;   // Vibrator output pin

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);  // button with pull-up
  pinMode(vibPin, OUTPUT);           // vibrator as output
  digitalWrite(vibPin, LOW);         // vibrator off initially
}

void loop() {
  int buttonState = digitalRead(buttonPin);

  if (buttonState == LOW) {  
    Serial.println("Button Pressed! Waiting 5 seconds...");
    
    delay(5000);  // wait 10 seconds

    Serial.println("Activating vibrator!");
    digitalWrite(vibPin, HIGH);   // Vibrator ON
    delay(1000);                  // Vibrate 1s
    digitalWrite(vibPin, LOW);    // Vibrator OFF

    delay(500); // debounce so it doesn’t re-trigger immediately
  }
}
