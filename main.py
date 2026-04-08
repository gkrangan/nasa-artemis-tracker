# Artemis2 Tracker

import requests
from datetime import datetime
import os

def fetch_artemis_telemetry():
    """
    Fetch real-time Artemis telemetry data.
    """
    url = "https://artemis.cdnspace.ca/api/arow"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch Artemis telemetry: {e}"}

def display_tracking_info():
    """
    Display tracking information for Artemis 2.
    """
    print("\n" + "="*50)
    print("      NASA ARTEMIS 2 TRACKING DASHBOARD")
    print("="*50)
    print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("-"*50)

    print("Mission Status:")
    print("  Status: Active - Return journey (Flight Day 7)")
    print("  Duration: ~10 days lunar flyby")
    print("  Crew: 4 astronauts")
    print("  Launched: April 1, 2026")

    print("\nReal-time Tracking Resources:")
    print("  - NASA Eyes 3D Solar System: https://eyes.nasa.gov/apps/solar-system/")
    print("  - Artemis II Mission Page: https://www.nasa.gov/artemis-ii/")
    print("  - JPL Horizons (Ephemeris): https://ssd.jpl.nasa.gov/horizons/")
    print("  - Mission Updates: https://www.nasa.gov/artemis-ii-news-and-updates/")

    # Fetch Artemis telemetry data
    telemetry_data = fetch_artemis_telemetry()
    
    print("\nArtemis Telemetry Data:")
    if "error" in telemetry_data:
        print(f"  Error: {telemetry_data['error']}")
    else:
        # Display key telemetry information
        position = telemetry_data.get('positionKm', {})
        print(f"  Position (km): X={position.get('x', 'N/A'):.1f}, Y={position.get('y', 'N/A'):.1f}, Z={position.get('z', 'N/A'):.1f}")
        
        euler = telemetry_data.get('eulerDeg', {})
        print(f"  Attitude (deg): Roll={euler.get('roll', 'N/A'):.1f}, Pitch={euler.get('pitch', 'N/A'):.1f}, Yaw={euler.get('yaw', 'N/A'):.1f}")
        
        rates = telemetry_data.get('rollRate', 'N/A'), telemetry_data.get('pitchRate', 'N/A'), telemetry_data.get('yawRate', 'N/A')
        print(f"  Rotation Rates (deg/s): Roll={rates[0]:.3f}, Pitch={rates[1]:.3f}, Yaw={rates[2]:.3f}")
        
        print(f"  Signal Light Time: {telemetry_data.get('signalLightTimeSec', 'N/A'):.3f} seconds")
        
        thrusters_active = sum(1 for t in telemetry_data.get('rcsThrusters', {}).get('thrusters', {}).values() if t)
        print(f"  RCS Thrusters Active: {thrusters_active}/14")
        
        print(f"  Spacecraft Mode: {telemetry_data.get('spacecraftMode', 'N/A')}")
        
        timestamp = telemetry_data.get('timestamp', 'N/A')
        print(f"  Last Update: {timestamp}")

    print("\nNote: For precise real-time position data, use the NASA Eyes application")
    print("      or JPL Horizons system with spacecraft ID '500@0' (Orion).")
    print("="*50 + "\n")

if __name__ == "__main__":
    display_tracking_info()