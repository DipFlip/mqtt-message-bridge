# MQTT Message Publisher/Reader

A simple Python MQTT publisher and reader system for sending messages over the internet. The publisher sends location-based timestamped messages that can be received by anyone running the reader script from anywhere in the world.

## Features

- Real-time message publishing over MQTT
- Internet-accessible (works across different networks)
- Simple to use - just two Python scripts
- No setup required with `uv`
- Uses public MQTT broker (no authentication needed)

## Quick Start

### With uv (recommended)

Install uv if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Run the publisher:
```bash
uv run --no-project publisher.py
```

Run the reader (can be on any machine with internet):
```bash
uv run --no-project reader.py
```

`uv` will automatically install the required `paho-mqtt` dependency.

### With traditional Python

Install dependencies:
```bash
pip install paho-mqtt
```

Run the publisher:
```bash
python3 publisher.py
```

Run the reader:
```bash
python3 reader.py
```

## How It Works

The system uses MQTT (Message Queue Telemetry Transport) protocol with a public broker (`broker.hivemq.com`):

1. **Publisher** - Connects to the MQTT broker and publishes messages every 5 seconds
   - Message format: `hello from Berkeley, time is YYYY-MM-DD HH:MM:SS`

2. **Reader** - Connects to the same MQTT broker and subscribes to receive all published messages
   - Displays messages in real-time as they arrive

Both scripts can run on different machines anywhere in the world as long as they have internet access.

## Requirements

- Python 3.7+
- `paho-mqtt` library (automatically installed by `uv`)

## Stopping the Scripts

Press `Ctrl+C` to stop either script gracefully.

Or kill background processes:
```bash
pkill -f publisher.py
pkill -f reader.py
```

## Configuration

You can customize the following in the scripts:

- `LOCATION` - Change the location name in `publisher.py`
- `BROKER` - Use a different MQTT broker
- `TOPIC` - Change the MQTT topic for different channels
- Publishing interval - Modify the `time.sleep(5)` value in `publisher.py`

## License

MIT
