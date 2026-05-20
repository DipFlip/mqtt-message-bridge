#!/usr/bin/env python3
"""Send a single lat/lon UDP packet, the same way lamp_autonomy does on source confirm.

Mirrors lamp_autonomy/tools/udp_publisher.py: no argparse loop, no broker, just
one JSON datagram to target:port and exit. Use it to smoke-test a receiver
(local_reader.py) without spinning up the autonomy stack.

Usage:
    python3 test_latlon_publish.py
    LOCAL_MESSAGE_TARGET=127.0.0.1 python3 test_latlon_publish.py
"""

import json
import os
import socket
from datetime import datetime, timezone


PORT = int(os.getenv("LOCAL_MESSAGE_PORT", "5005"))
SOURCE = os.getenv("LOCAL_MESSAGE_SOURCE", "nglamp")
TARGET = os.getenv("LOCAL_MESSAGE_TARGET", "10.0.0.136")

LAT = float(os.getenv("LOCAL_MESSAGE_LAT", "37.8715"))
LON = float(os.getenv("LOCAL_MESSAGE_LON", "-122.2730"))


def _is_broadcast_target(target):
    return target in {"<broadcast>", "broadcast", "255.255.255.255"}


def send_latlon(lat, lon, target=TARGET, port=PORT, source=SOURCE):
    actual_target = "255.255.255.255" if _is_broadcast_target(target) else target

    payload = json.dumps(
        {
            "type": "latlon",
            "source": source,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "lat": lat,
            "lon": lon,
        },
        separators=(",", ":"),
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        if _is_broadcast_target(target):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(payload.encode("utf-8"), (actual_target, port))
    finally:
        sock.close()

    return payload


if __name__ == "__main__":
    sent = send_latlon(LAT, LON)
    print(f"Sent to {TARGET}:{PORT} -> {sent}")
