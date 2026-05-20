#!/usr/bin/env python3
"""Local UDP publisher for broadcast or direct unicast messages."""

import argparse
import json
import os
import socket
import time
from datetime import datetime, timezone

# Configuration
DEFAULT_PORT = int(os.getenv("LOCAL_MESSAGE_PORT", "5005"))
DEFAULT_LOCATION = os.getenv("LOCAL_MESSAGE_SOURCE", "nglamp")
DEFAULT_INTERVAL = float(os.getenv("LOCAL_MESSAGE_INTERVAL", "5"))
DEFAULT_TARGET = os.getenv("LOCAL_MESSAGE_TARGET", "10.0.0.136")


def env_float(name):
    value = os.getenv(name)
    return float(value) if value else None


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send local UDP messages, including lat/lon coordinates."
    )
    parser.add_argument(
        "--target",
        default=DEFAULT_TARGET,
        help="Destination IP or '<broadcast>' (default: %(default)s)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="UDP destination port (default: %(default)s)",
    )
    parser.add_argument(
        "--source",
        default=DEFAULT_LOCATION,
        help="Source name included in JSON messages (default: %(default)s)",
    )
    parser.add_argument(
        "--lat",
        type=float,
        default=env_float("LOCAL_MESSAGE_LAT"),
        help="Latitude to send",
    )
    parser.add_argument(
        "--lon",
        type=float,
        default=env_float("LOCAL_MESSAGE_LON"),
        help="Longitude to send",
    )
    parser.add_argument(
        "--message",
        help="Optional plain text message. If omitted with --lat/--lon, JSON is sent.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_INTERVAL,
        help="Seconds between repeated sends (default: %(default)s)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Send one message and exit",
    )
    return parser.parse_args()


def is_broadcast_target(target):
    return target in {"<broadcast>", "broadcast", "255.255.255.255"}


def get_local_ip(target, port):
    probe_target = "8.8.8.8" if is_broadcast_target(target) else target
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect((probe_target, port))
            return sock.getsockname()[0]
    except OSError:
        return "unknown"


def build_message(args):
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if args.message:
        return args.message

    if args.lat is not None or args.lon is not None:
        if args.lat is None or args.lon is None:
            raise SystemExit("Provide both --lat and --lon, or neither.")

        return json.dumps(
            {
                "type": "latlon",
                "source": args.source,
                "timestamp": timestamp,
                "lat": args.lat,
                "lon": args.lon,
            },
            separators=(",", ":"),
        )

    return json.dumps(
        {
            "type": "heartbeat",
            "source": args.source,
            "timestamp": timestamp,
            "message": f"hello from {args.source}",
        },
        separators=(",", ":"),
    )


def main():
    args = parse_args()
    target = "255.255.255.255" if is_broadcast_target(args.target) else args.target

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if is_broadcast_target(args.target):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Get local IP
    local_ip = get_local_ip(args.target, args.port)

    print("Local Publisher Started")
    print(f"Local IP: {local_ip}")
    print(f"Sending to {target}:{args.port}")
    print(f"Source: {args.source}")
    print("\nPress Ctrl+C to stop.\n")

    try:
        while True:
            message = build_message(args)

            # Send message
            sock.sendto(message.encode("utf-8"), (target, args.port))
            print(f"Sent: {message}")

            if args.once:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n\nStopping publisher...")
    finally:
        sock.close()
        print("Publisher stopped")

if __name__ == "__main__":
    main()
