from flask import Flask, request, jsonify
from awscrt import mqtt
from awsiot import mqtt_connection_builder
import sqlite3
import datetime
import json
import threading
import os

app = Flask(__name__)
DB_NAME = "nami.db"

# --- Absolute Path Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(BASE_DIR, "certs")

# --- Auto-detect Certificates ---
def find_cert_file(extension_keywords):
    """Find a certificate/key file in certs/ that matches keywords."""
    for f in os.listdir(CERT_DIR):
        if all(kw in f for kw in extension_keywords):
            return os.path.join(CERT_DIR, f)
    return None

PATH_TO_CERT = find_cert_file(["cert", ".pem"])       # e.g. nami.cert.pem
PATH_TO_KEY = find_cert_file(["private", ".key"])     # e.g. nami.private.key
PATH_TO_ROOT = os.path.join(CERT_DIR, "AmazonRootCA1.pem")

# Ensure Root CA exists, download if missing
if not os.path.exists(PATH_TO_ROOT):
    print("🌍 Downloading AmazonRootCA1.pem...")
    os.system(f"wget https://www.amazontrust.com/repository/AmazonRootCA1.pem -O {PATH_TO_ROOT}")

print("🔑 Using certificates:")
print(f"   Device Cert: {PATH_TO_CERT}")
print(f"   Private Key: {PATH_TO_KEY}")
print(f"   Root CA    : {PATH_TO_ROOT}")

# --- MQTT Setup ---
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint="a1x93bx6u0faww-ats.iot.us-east-1.amazonaws.com",  # Your AWS IoT Core endpoint
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    ca_filepath=PATH_TO_ROOT,
    client_id="nami-client",
    clean_session=False,
    keep_alive_secs=30
)

# Connect once at startup (non-blocking)
def connect_mqtt():
    print("🔌 Connecting to AWS IoT Core...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("✅ Connected to AWS IoT Core!")

threading.Thread(target=connect_mqtt).start()

# --- Initialize DB ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device TEXT,
                    event TEXT,
                    lat REAL,
                    lng REAL,
                    timestamp_s INTEGER,
                    created_at TEXT
                )''')
    conn.commit()
    conn.close()

# --- API Route ---
@app.route("/api/event", methods=["POST"])
def receive_event():
    data = request.json
    device = data.get("device")
    event = data.get("event")
    lat = data.get("lat")
    lng = data.get("lng")
    timestamp_s = data.get("timestamp_s")
    created_at = datetime.datetime.utcnow().isoformat()

    # Save to DB
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO events (device, event, lat, lng, timestamp_s, created_at) VALUES (?, ?, ?, ?, ?, ?)",
              (device, event, lat, lng, timestamp_s, created_at))
    conn.commit()
    conn.close()

    # Publish to AWS IoT Core
    payload = {
        "device": device,
        "event": event,
        "lat": lat,
        "lng": lng,
        "timestamp_s": timestamp_s,
        "created_at": created_at
    }

    mqtt_connection.publish(
        topic="nami/events",
        payload=json.dumps(payload),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    print("🚨 New Event Received & Published to AWS IoT!")
    print(f"   Device: {device}")
    print(f"   Event: {event}")
    print(f"   Location: {lat}, {lng}")
    print(f"   Timestamp: {timestamp_s}")
    print("   ✅ Stored in SQLite and sent to IoT Core\n")

    return jsonify({"status": "success", "message": "Event stored and published!"})

# --- Start Server ---
if __name__ == "__main__":
    init_db()
    print("📡 Flask server started. Listening on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
