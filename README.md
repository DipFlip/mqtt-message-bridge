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

Perfect for machines on the same WiFi/LAN, or for two routed local subnets.
Uses UDP on port 5005. It can broadcast on one LAN or send directly to a target IP.

**Publisher:**
```bash
uv run --no-project local_publisher.py
```

**Reader (on another machine on same network):**
```bash
uv run --no-project local_reader.py
```

The publisher broadcasts to the local network and the reader automatically receives messages.

**Direct coordinate send:**
```bash
uv run --no-project local_publisher.py --target 10.0.0.136 --lat 37.8715 --lon -122.2730 --once
```

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
- **local_publisher.py** - Sends UDP messages on port 5005 using broadcast or direct unicast
- **local_reader.py** - Listens for UDP messages on port 5005
- No internet required
- Broadcast works on one LAN; routed subnets should use `--target <receiver-ip>`

### Local setup: nglamp to Spot Dog

Goal:
- Sender: `nglamp` Ubuntu machine at `10.0.0.127`
- Receiver: Spot Dog Mac at `10.0.0.136`
- Both machines are on the same `10.0.0.0/24` local network

On the Spot Dog Mac, run the reader:
```bash
python3 local_reader.py --bind 0.0.0.0 --port 5005
```

Then send a coordinate from `nglamp` to the Spot Dog Mac:
```bash
python3 local_publisher.py --lat 37.8715 --lon -122.2730 --once
```

For repeated sends, omit `--once` and optionally set `--interval`:
```bash
python3 local_publisher.py --lat 37.8715 --lon -122.2730 --interval 5
```

The publisher defaults to `--target 10.0.0.136`, so no route changes or temporary Mac router are needed for this same-subnet setup. Use `--target <ip>` only if Spot Dog gets a different address.

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
- `LOCAL_MESSAGE_PORT` - UDP port (default: 5005)
- `LOCAL_MESSAGE_SOURCE` - Source name (default: `nglamp`)
- `LOCAL_MESSAGE_TARGET` - Target IP or `<broadcast>` (default: `10.0.0.136`)
- `LOCAL_MESSAGE_LAT` - Latitude
- `LOCAL_MESSAGE_LON` - Longitude
- `LOCAL_MESSAGE_INTERVAL` - Seconds between messages (default: 5)

**Internet Scripts:**
- `LOCATION` - Change the location name in `publisher.py`
- `BROKER` - Use a different MQTT broker (default: broker.hivemq.com)
- `TOPIC` - Change the MQTT topic for different channels
- Publishing interval - Modify `time.sleep(5)` in `publisher.py`

## License

MIT
