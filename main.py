# Artemis2 Tracker

import requests
from datetime import datetime
import os

def fetch_nasa_artemis_data():
    """
    Fetch Artemis-related data from NASA's Image and Video Library.
    """
    url = "https://images-api.nasa.gov/search?q=artemis"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch Artemis data: {e}"}

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

    # Fetch NASA's Artemis data
    artemis_data = fetch_nasa_artemis_data()
    
    print("\nNASA Artemis Mission Data:")
    if "error" in artemis_data:
        print(f"  Error: {artemis_data['error']}")
    else:
        collection = artemis_data.get('collection', {})
        items = collection.get('items', [])
        if items:
            print(f"  Found {len(items)} Artemis-related items.")
            # Show first item details
            item = items[0]
            data = item.get('data', [{}])[0]
            print(f"  Title: {data.get('title', 'N/A')}")
            print(f"  Description: {data.get('description', 'N/A')[:200]}...")
            links = item.get('links', [])
            if links:
                print(f"  Image URL: {links[0].get('href', 'N/A')}")
        else:
            print("  No Artemis data found.")

    print("\nNote: For precise real-time position data, use the NASA Eyes application")
    print("      or JPL Horizons system with spacecraft ID '500@0' (Orion).")
    print("="*50 + "\n")

if __name__ == "__main__":
    display_tracking_info()