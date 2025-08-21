from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)
DB_NAME = "nami.db"

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

    # Print to console for debugging
    print("🚨 New Event Received!")
    print(f"   Device: {device}")
    print(f"   Event: {event}")
    print(f"   Location: {lat}, {lng}")
    print(f"   Timestamp: {timestamp_s}")
    print("   ✅ Stored in SQLite\n")

    return jsonify({"status": "success", "message": "Event stored!"})

if __name__ == "__main__":
    init_db()
    print("📡 Flask server started. Listening on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
