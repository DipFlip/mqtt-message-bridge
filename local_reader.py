#!/usr/bin/env python3
"""Local UDP reader for broadcast or direct unicast messages."""

import argparse
import json
import os
import socket

# Configuration
DEFAULT_PORT = int(os.getenv("LOCAL_MESSAGE_PORT", "5005"))
DEFAULT_BIND = os.getenv("LOCAL_MESSAGE_BIND", "0.0.0.0")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Receive local UDP messages, including lat/lon coordinates."
    )
    parser.add_argument(
        "--bind",
        default=DEFAULT_BIND,
        help="Address to bind on (default: %(default)s)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="UDP listen port (default: %(default)s)",
    )
    return parser.parse_args()


def format_message(payload):
    try:
        message = json.loads(payload)
    except json.JSONDecodeError:
        return payload

    if isinstance(message, dict) and message.get("type") == "latlon":
        return (
            "latlon "
            f"source={message.get('source', 'unknown')} "
            f"lat={message.get('lat')} "
            f"lon={message.get('lon')} "
            f"timestamp={message.get('timestamp', 'unknown')}"
        )

    return json.dumps(message, sort_keys=True)

def main():
    args = parse_args()

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Bind to the listen port
    sock.bind((args.bind, args.port))

    print("Local Reader Started")
    print(f"Listening on {args.bind}:{args.port}")
    print("\nWaiting for messages... Press Ctrl+C to stop.\n")

    try:
        while True:
            # Receive data
            data, addr = sock.recvfrom(4096)
            payload = data.decode("utf-8", errors="replace")
            sender_ip = addr[0]

            print(f"Received from {sender_ip}: {format_message(payload)}")

    except KeyboardInterrupt:
        print("\n\nStopping reader...")
    finally:
        sock.close()
        print("Reader stopped")

if __name__ == "__main__":
    main()
