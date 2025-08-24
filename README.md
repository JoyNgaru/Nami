# Nami – Personal Safety IoT Device

Nami is a **personal safety IoT device** that sends a discreet SOS signal when you’re in distress.  
With a single press of the Nami button, your **location data** is sent to your emergency contact.  
Once the message is received, the pendant vibrates to confirm that your SOS alert has been delivered.  

---

## 🚀 Features
- Small, portable, and wearable IoT device
- One-press **SOS button** for emergencies
- Sends **real-time location** to a predefined contact
- **Vibration feedback** when the alert is successfully delivered
- Cloud-enabled for **backup and notifications**

---

## 🛠️ Tech Stack
- **Hardware:** ESP32 / Raspberry Pi / IoT module
- **Backend:** Flask + SQLite (local) / AWS (cloud)
- **Cloud Services:**
  - AWS S3 → Backup of data
  - AWS SNS → Notifications (SMS/Email alerts)
  - AWS IoT Core → Device connectivity
- **Dashboard:** Web-based (Flask) with charts for sensor data & activity

---

## 📂 Project Structure
