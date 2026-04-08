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

def fetch_artemis_orbit():
    """
    Fetch Artemis orbit data.
    """
    url = "https://artemis.cdnspace.ca/api/orbit"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch Artemis orbit data: {e}"}

def fetch_artemis_state():
    """
    Fetch Artemis state vector data.
    """
    url = "https://artemis.cdnspace.ca/api/state"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch Artemis state data: {e}"}

def fetch_artemis_all():
    """
    Fetch comprehensive Artemis data including DSN communication status.
    """
    url = "https://artemis.cdnspace.ca/api/all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch Artemis all data: {e}"}

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

    # Fetch Artemis orbit data
    orbit_data = fetch_artemis_orbit()
    
    print("\nArtemis Orbit Data:")
    if "error" in orbit_data:
        print(f"  Error: {orbit_data['error']}")
    else:
        # Display orbit information
        met_hours = orbit_data.get('metMs', 0) / (1000 * 3600)  # Convert ms to hours
        print(f"  Mission Elapsed Time: {met_hours:.1f} hours")
        print(f"  Speed: {orbit_data.get('speedKmS', 'N/A'):.3f} km/s ({orbit_data.get('speedKmH', 'N/A'):.0f} km/h)")
        print(f"  Relative to Moon: {orbit_data.get('moonRelSpeedKmH', 'N/A'):.0f} km/h")
        print(f"  Altitude: {orbit_data.get('altitudeKm', 'N/A'):.0f} km")
        print(f"  Distance to Earth: {orbit_data.get('earthDistKm', 'N/A'):.0f} km")
        print(f"  Distance to Moon: {orbit_data.get('moonDistKm', 'N/A'):.0f} km")
        print(f"  Periapsis: {orbit_data.get('periapsisKm', 'N/A'):.0f} km")
        print(f"  Apoapsis: {orbit_data.get('apoapsisKm', 'N/A'):.0f} km")
        print(f"  G-Force: {orbit_data.get('gForce', 'N/A'):.6f} g")

    # Fetch Artemis state data
    state_data = fetch_artemis_state()
    
    print("\nArtemis State Vector:")
    if "error" in state_data:
        print(f"  Error: {state_data['error']}")
    else:
        # Display state vector information
        state_vector = state_data.get('stateVector', {})
        met_hours = state_vector.get('metMs', 0) / (1000 * 3600)  # Convert ms to hours
        print(f"  Mission Elapsed Time: {met_hours:.1f} hours")
        
        position = state_vector.get('position', {})
        print(f"  Position (km): X={position.get('x', 'N/A'):.1f}, Y={position.get('y', 'N/A'):.1f}, Z={position.get('z', 'N/A'):.1f}")
        
        velocity = state_vector.get('velocity', {})
        print(f"  Velocity (km/s): X={velocity.get('x', 'N/A'):.3f}, Y={velocity.get('y', 'N/A'):.3f}, Z={velocity.get('z', 'N/A'):.3f}")
        
        moon_pos = state_data.get('moonPosition', {})
        print(f"  Moon Position (km): X={moon_pos.get('x', 'N/A'):.1f}, Y={moon_pos.get('y', 'N/A'):.1f}, Z={moon_pos.get('z', 'N/A'):.1f}")
        
        timestamp = state_vector.get('timestamp', 'N/A')
        print(f"  State Timestamp: {timestamp}")

    # Fetch Artemis all data (includes DSN communication status)
    all_data = fetch_artemis_all()
    
    print("\nDeep Space Network (DSN) Communication:")
    if "error" in all_data:
        print(f"  Error: {all_data['error']}")
    else:
        dsn_data = all_data.get('dsn', {})
        dishes = dsn_data.get('dishes', [])
        print(f"  Signal Active: {dsn_data.get('signalActive', 'N/A')}")
        print(f"  Timestamp: {dsn_data.get('timestamp', 'N/A')}")
        print(f"  Active Dishes:")
        
        for dish in dishes:
            dish_name = dish.get('dish', 'Unknown')
            station = dish.get('stationName', 'Unknown')
            downlink_active = dish.get('downlinkActive', False)
            uplink_active = dish.get('uplinkActive', False)
            
            if downlink_active or uplink_active:
                status = []
                if downlink_active:
                    rate = dish.get('downlinkRate', 0)
                    band = dish.get('downlinkBand', '')
                    status.append(f"DL:{rate/1e6:.1f}Mbps({band})")
                if uplink_active:
                    band = dish.get('uplinkBand', '')
                    status.append(f"UL({band})")
                
                az = dish.get('azimuth', 'N/A')
                el = dish.get('elevation', 'N/A')
                range_km = dish.get('rangeKm', 'N/A')
                rtlt = dish.get('rtltSeconds', 'N/A')
                
                print(f"    {dish_name} ({station}): {', '.join(status)}")
                print(f"      Position: Az={az}°, El={el}°  |  Range: {range_km}km  |  RTL: {rtlt}s")

    print("\nNote: For precise real-time position data, use the NASA Eyes application")
    print("      or JPL Horizons system with spacecraft ID '500@0' (Orion).")
    print("="*50 + "\n")

if __name__ == "__main__":
    display_tracking_info()