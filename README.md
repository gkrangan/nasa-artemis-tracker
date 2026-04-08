# Artemis2 Tracker

A Python application to track NASA's Artemis2 spacecraft using NASA's Open APIs.

## Features

- Display mission status and tracking information
- Fetch real-time Artemis telemetry data
- Links to NASA resources for additional tracking

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Set your NASA API key (optional, uses DEMO_KEY if not set):
```bash
export NASA_API_KEY=your_api_key_here
```

Run the tracker:
```bash
python main.py
```

This will display the current status of Artemis 2 and real-time telemetry data from the Artemis API.

## API Key

Get your free API key from [NASA's API Portal](https://api.nasa.gov/). The app uses the DEMO_KEY by default, which has rate limits.

## Resources

- [NASA Artemis II Mission](https://www.nasa.gov/artemis-ii/)
- [NASA Eyes 3D Tracker](https://eyes.nasa.gov/apps/solar-system/)
- [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/)
- [NASA Open APIs](https://api.nasa.gov/)
