#!/usr/bin/env python3
"""
Local network reader using UDP broadcast.
Listens for messages on the local network from local_publisher.py
No IP address needed - automatically receives broadcast messages.
"""

import socket

# Configuration
BROADCAST_PORT = 5005

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the broadcast port
    sock.bind(('', BROADCAST_PORT))

    print(f"Local Reader Started")
    print(f"Listening for broadcasts on port {BROADCAST_PORT}")
    print(f"\nWaiting for messages... Press Ctrl+C to stop.\n")

    try:
        while True:
            # Receive data
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            sender_ip = addr[0]

            print(f"Received from {sender_ip}: {message}")

    except KeyboardInterrupt:
        print("\n\nStopping reader...")
    finally:
        sock.close()
        print("Reader stopped")

if __name__ == "__main__":
    main()
