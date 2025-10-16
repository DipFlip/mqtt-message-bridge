# Message Publisher/Reader

Simple Python scripts for sending messages between machines. Choose between:
- **Internet mode** (MQTT) - Works across different networks worldwide
- **Local network mode** (UDP) - Works on same WiFi/LAN without internet

## Features

- Real-time message publishing
- Two modes: Internet (MQTT) or Local Network (UDP)
- Simple to use - just Python scripts
- No setup required with `uv`
- Shows sender's location and timestamp

## Quick Start

### Mode 1: Local Network (No Internet Required)

Perfect for machines on the same WiFi/LAN. Uses UDP broadcast - no IP address needed!

**Publisher:**
```bash
uv run --no-project local_publisher.py
```

**Reader (on another machine on same network):**
```bash
uv run --no-project local_reader.py
```

The publisher broadcasts to the local network and the reader automatically receives messages.

### Mode 2: Internet (Across Different Networks)

Works anywhere in the world with internet connection. Uses MQTT public broker.

**Publisher:**
```bash
uv run publisher.py
```

**Reader (can be anywhere with internet):**
```bash
uv run reader.py
```

### Installation

If you don't have `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`uv` automatically installs dependencies (paho-mqtt for internet mode, none needed for local mode).

Alternatively with pip:
```bash
pip install paho-mqtt  # Only needed for internet mode
python3 local_publisher.py  # or publisher.py
```

## How It Works

### Local Network Mode
- **local_publisher.py** - Broadcasts UDP messages on port 5005 to local network
- **local_reader.py** - Listens for UDP broadcasts on the same network
- No internet required, no IP address configuration needed
- Works on same WiFi/LAN

### Internet Mode
- **publisher.py** - Connects to public MQTT broker (`broker.hivemq.com`)
- **reader.py** - Connects to same broker and receives messages
- Works across different networks worldwide
- Requires internet connection

## Requirements

- Python 3.7+
- **Local mode:** No dependencies
- **Internet mode:** `paho-mqtt` library (automatically installed by `uv`)

## Stopping the Scripts

Press `Ctrl+C` to stop any script gracefully.

## Configuration

**Local Network Scripts:**
- `BROADCAST_PORT` - UDP port (default: 5005)
- `LOCATION` - Location name
- `BROADCAST_INTERVAL` - Seconds between messages (default: 5)

**Internet Scripts:**
- `LOCATION` - Change the location name in `publisher.py`
- `BROKER` - Use a different MQTT broker (default: broker.hivemq.com)
- `TOPIC` - Change the MQTT topic for different channels
- Publishing interval - Modify `time.sleep(5)` in `publisher.py`

## License

MIT
