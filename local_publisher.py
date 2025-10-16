#!/usr/bin/env python3
"""
Local network publisher using UDP broadcast.
Broadcasts messages on the local network that any reader can receive.
No need to specify IP - uses UDP broadcast.
"""

import socket
import time
from datetime import datetime

# Configuration
BROADCAST_PORT = 5005
LOCATION = "Berkeley"
BROADCAST_INTERVAL = 5  # seconds

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Get local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "unknown"

    print(f"Local Publisher Started")
    print(f"Local IP: {local_ip}")
    print(f"Broadcasting on port {BROADCAST_PORT}")
    print(f"Location: {LOCATION}")
    print(f"\nPress Ctrl+C to stop.\n")

    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"hello from {LOCATION}, time is {current_time}"

            # Broadcast message
            sock.sendto(message.encode('utf-8'), ('<broadcast>', BROADCAST_PORT))
            print(f"Sent: {message}")

            time.sleep(BROADCAST_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nStopping publisher...")
    finally:
        sock.close()
        print("Publisher stopped")

if __name__ == "__main__":
    main()
