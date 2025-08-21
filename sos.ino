#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// --- WiFi ---
const char* ssid = "Nana";
const char* password = "qwertyuiop";
const char* serverUrl = "http://10.115.12.201:5000/api/event"; 

// --- Pins ---
#define BUTTON_PIN  4   // Button (using internal pullup)
#define VIB_PIN     5   // Vibrator motor

// --- State ---
bool sosTriggered = false;
unsigned long sosTime = 0;

void setup() {
  Serial.begin(115200);

  // Init button + vibrator
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(VIB_PIN, OUTPUT);
  digitalWrite(VIB_PIN, LOW);

  // Connect WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Connected to WiFi!");
}

void loop() {
  int buttonState = digitalRead(BUTTON_PIN);

  // Button pressed
  if (buttonState == LOW && !sosTriggered) {
    Serial.println("🚨 SOS Button Pressed!");
    sosTriggered = true;
    sosTime = millis();
  }

  // After 10 seconds, vibrate and send event
  if (sosTriggered && millis() - sosTime >= 10000) {
    Serial.println("⏳ 10 seconds passed, activating vibrator...");
    
    digitalWrite(VIB_PIN, HIGH); 
    Serial.println("🔔 Vibrator ON");
    delay(2000);                 // buzz 2 sec
    digitalWrite(VIB_PIN, LOW);
    Serial.println("🔕 Vibrator OFF");

    Serial.println("📡 Sending SOS event to server...");
    sendEventToServer();

    sosTriggered = false; // reset
  }
}

void sendEventToServer() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ WiFi not connected!");
    return;
  }

  // Simulated GPS coords (Brookside Dr, Nairobi)
  float lat = -1.2683;
  float lng = 36.8046;

  // Create JSON
  StaticJsonDocument<256> doc;
  doc["device"] = "nami_esp32";
  doc["event"] = "SOS";
  doc["lat"] = lat;
  doc["lng"] = lng;
  doc["timestamp_s"] = millis() / 1000;

  String jsonString;
  serializeJson(doc, jsonString);

  // Send HTTP POST
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(jsonString);
  if (httpResponseCode > 0) {
    Serial.print("✅ Server response: ");
    Serial.println(http.getString());
  } else {
    Serial.print("❌ Error sending: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}
