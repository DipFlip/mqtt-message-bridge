#!/usr/bin/env python3
"""
Reader script that subscribes to messages from the publisher.
This can be run from anywhere with internet access to receive messages.
"""

import sys
sys.stdout = sys.stderr = open(sys.stdout.fileno(), 'w', buffering=1)

import paho.mqtt.client as mqtt
import time

# Public MQTT broker (same as publisher)
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "berkeley/pinglatlon/messages"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {BROKER}")
        print(f"Subscribed to topic: {TOPIC}")
        print("\nWaiting for messages... Press Ctrl+C to stop.\n")
        # Subscribe to topic
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback when a message is received"""
    message = msg.payload.decode('utf-8')
    print(f"Received: {message}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscription confirmed (QoS: {granted_qos[0]})")

def main():
    # Create MQTT client
    client = mqtt.Client(client_id="berkeley_reader", clean_session=True)

    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    try:
        # Connect to broker
        print(f"Connecting to {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, 60)

        # Start network loop (blocking)
        # This will keep the script running and listening for messages
        client.loop_forever()

    except KeyboardInterrupt:
        print("\nStopping reader...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("Disconnected from broker")

if __name__ == "__main__":
    main()
