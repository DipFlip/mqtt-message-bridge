#!/usr/bin/env python3
# /// script
# dependencies = ["paho-mqtt"]
# ///
"""
Publisher script that sends messages with location and timestamp to an MQTT broker.
Messages can be received by anyone running the reader.py script.
"""

import sys
sys.stdout = sys.stderr = open(sys.stdout.fileno(), 'w', buffering=1)

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json

# Public MQTT broker (free to use, no authentication required)
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "berkeley/pinglatlon/messages"

# Location information
LOCATION = "Berkeley"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {BROKER}")
        print(f"Publishing to topic: {TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message published (ID: {mid})")

def main():
    # Create MQTT client
    client = mqtt.Client(client_id="berkeley_publisher", clean_session=True)

    # Set callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        # Connect to broker
        print(f"Connecting to {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, 60)

        # Start network loop in background
        client.loop_start()

        # Wait for connection
        time.sleep(2)

        print("\nStarting to publish messages. Press Ctrl+C to stop.\n")

        # Publish messages every 5 seconds
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"hello from {LOCATION}, time is {current_time}"

            # Publish the message
            result = client.publish(TOPIC, message, qos=1)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Sent: {message}")
            else:
                print(f"Failed to send message")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nStopping publisher...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from broker")

if __name__ == "__main__":
    main()
