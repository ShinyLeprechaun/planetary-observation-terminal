import requests
import json
import os # For taking control of the terminal screen
from datetime import datetime, timedelta, timezone
import math

# --- ANSI Color Codes ---
# These special strings tell the terminal to change text properties
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

PLANET_IDS = {
    "mercury": "199",
    "venus": "299",
    "earth": "399",
    "mars": "499",
    "jupiter": "599",
    "saturn": "699",
    "uranus": "799",
    "neptune": "899"
}

def clear_screen():
    # 'nt' is the internal name for Windows
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    # Multi-line string for ASCII Art
    header = f"""{GREEN}{BOLD}
 _______         _               _______         _               _______        _________     
(  ____ )       ( \             (  ___  )       ( (    /|       (  ____ \       \__   __/     
| (    )|       | (             | (   ) |       |  \  ( |       | (    \/          ) (        
| (____)|       | |             | (___) |       |   \ | |       | (__              | |        
|  _____)       | |             |  ___  |       | (\ \) |       |  __)             | |        
| (             | |             | (   ) |       | | \   |       | (                | |        
| )         _   | (____/\   _   | )   ( |   _   | )  \  |   _   | (____/\   _      | |      _ 
|/         (_)  (_______/  (_)  |/     \|  (_)  |/    )_)  (_)  (_______/  (_)     )_(     (_)

=== Planetary Location And Network Ephemeris Terminal ===
> Telemetry data courtesy of NASA JPL Horizons API. Use fullscreen for best visual.
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠠⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠠⡐⣐⣧⣾⣾⣿⣿⣿⣿⣿⣿⣷⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣥⣤⣴⢶⣶⣶⣶⣶⠾⠞⠓⠂⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣥⠤⠤⢶⡂⠀⠄⠀⠄⠀⠀⠀⣄⣔⣤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠄⡀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⣿⣿⣛⣻⡿⣿⡷⣶⢍⠢⡀⣀⣤⢲⡆⢹⢾⢸⠂⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠉⠛⣿⣎⢻⠞⣣⣄⡷⢿⠿⣼⢃⣓⢎⠆⠀⠀
⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠆⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣟⢦⣶⣿⢝⠞⡨⣳⡿⢑⣹⠟⠁⠀⠀⠀
⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⢾⡻⣙⢔⢨⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⣴⣟⣵⡿⣻⣕⢥⣾⢞⣵⡣⠞⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣶⢟⡭⡺⣝⣝⣾⡾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⡿⣞⣿⡾⡿⣝⣼⡪⣟⣽⡾⠟⠁⠀⢀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡠⣴⠟⣩⣾⠗⡩⣪⣾⡿⣻⡾⠛⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⣯⣗⣯⣷⡟⣏⣧⡷⣟⣫⡵⠞⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡪⠞⠡⣚⡻⠥⡜⣮⣟⣾⢼⣿⡅⠀⢹⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢿⡞⣿⣻⢼⢷⣛⣯⡷⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣱⣍⣡⣁⡮⡷⢺⣟⢿⣷⣻⣮⣻⡿⣶⣤⣿⣿⣟⣿⣿⣿⣛⣻⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣧⣿⣷⣫⣿⢷⡟⢏⡙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣼⢶⣟⢼⡻⣺⣝⡷⣨⢓⠥⡟⣻⣾⣿⠿⠿⣷⣶⣶⣾⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣯⣿⣿⣿⣟⡻⠹⣓⣺⣵⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⠿⣗⡽⣵⡌⣝⡛⣷⡿⢿⣤⣿⣿⣷⣾⡿⢿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⣤⡷⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠉⠙⠚⠛⠛⠿⠿⠿⠿⠿⠿⠟⠛⠛⠛⠛⠋⠉⠩⢗⢽⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠙⠋⠟⠋⠛⠛⡛⠛⠉⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠁⠀⠀⠀⠀⠀⠀⠄⠂
⠀⠄⠀⠀⠀⠐⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠈⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠂⠀⠀⠂⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠁⡀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠂⠀⠀⠀⠠⠀⠀⠀⠀                                 
{RESET}
"""
    print(header)

def parse_vector_data(raw_data):
    start_idx = raw_data.find("$$SOE")
    end_idx = raw_data.find("$$EOE")

    if start_idx == -1 or end_idx == -1:
        return None 
    
    ephem_block = raw_data[start_idx:end_idx]
    lines = ephem_block.split("\n")
    vectors = {}

    for line in lines:
        line = line.strip()
        if line.startswith("X ="):
            x_part, rest = line.split("Y =")
            y_part, z_part = rest.split("Z =")
            vectors['X'] = float(x_part.replace("X =", "").strip())
            vectors['Y'] = float(y_part.strip())
            vectors['Z'] = float(z_part.strip())

        elif line.startswith("VX="):
            vx_part, rest = line.split("VY=")
            vy_part, vz_part = rest.split("VZ=")
            vectors['VX'] = float(vx_part.replace("VX=", "").strip())
            vectors['VY'] = float(vy_part.strip())
            vectors['VZ'] = float(vz_part.strip())
            
    return vectors

def parse_visibility_data(raw_data):
    start_idx = raw_data.find("$$SOE")
    end_idx = raw_data.find("$$EOE")

    if start_idx == -1 or end_idx == -1:
        return None

    ephem_block = raw_data[start_idx + 5:end_idx].strip()
    lines = ephem_block.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        if len(parts) >= 4:
            try:
                ob_lon = float(parts[-2])
                ob_lat = float(parts[-1])
                return {"lon": ob_lon, "lat": ob_lat}
            except ValueError:
                pass
    return None

def get_planet_data(target_id):
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    now = datetime.now(timezone.utc)
    tomorrow = now + timedelta(days=1)

    start_str = now.strftime("'%Y-%m-%d %H:%M:%S'")
    display_time = now.strftime("%b %d, %Y at %H:%M:%S UTC")
    stop_str = tomorrow.strftime("'%Y-%m-%d %H:%M:%S'")

    # First Request: Vectors
    params = {
        "format": "json",
        "COMMAND": target_id,
        "OBJ_DATA": "YES",      
        "MAKE_EPHEM": "YES",     
        "EPHEM_TYPE": "VECTORS", 
        "CENTER": "@10",         
        "START_TIME": start_str, 
        "STOP_TIME": stop_str, 
        "STEP_SIZE": "1d" 
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        raw_result = data.get('result', '')
        parsed_data = parse_vector_data(raw_result)
        
        if parsed_data:
            dist_sun = math.sqrt(parsed_data['X']**2 + parsed_data['Y']**2 + parsed_data['Z']**2)
            speed = math.sqrt(parsed_data['VX']**2 + parsed_data['VY']**2 + parsed_data['VZ']**2)
            
            print(f"{GREEN}{BOLD}\n[+] HIGHLIGHT DATA -------------------------{RESET}{GREEN}")
            print(f"    Live as of:        {display_time}")
            print(f"    Distance from Sun: {dist_sun:,.2f} km")
            print(f"    Current Velocity:  {speed:,.2f} km/s")
            
            print(f"{BOLD}\n[+] SOLAR COORDINATES ----------------------{RESET}{GREEN}")
            print(f"    X: {parsed_data['X']:,.2f} km")
            print(f"    Y: {parsed_data['Y']:,.2f} km")
            print(f"    Z: {parsed_data['Z']:,.2f} km")
            
            # Second Request: visibility
            if target_id != "399":
                vis_params = {
                    "format": "json",
                    "COMMAND": target_id,
                    "OBJ_DATA": "NO",
                    "MAKE_EPHEM": "YES",
                    "EPHEM_TYPE": "OBSERVER",
                    "CENTER": "500@399", 
                    "QUANTITIES": "14",  
                    "START_TIME": start_str,
                    "STOP_TIME": stop_str,
                    "STEP_SIZE": "1d"
                }
                
                vis_response = requests.get(url, params=vis_params)
                if vis_response.status_code == 200:
                    vis_data = vis_response.json()
                    vis_parsed = parse_visibility_data(vis_data.get('result', ''))
                    
                    if vis_parsed:
                        lat = vis_parsed['lat']
                        raw_lon = vis_parsed['lon']
                        
                        # nasa outputs 0 to 360, google needs -180 to 180
                        lon = (raw_lon + 180) % 360 - 180
                        
                        # Format coordinates (North/South, East/West)
                        lat_str = f"{abs(lat):.2f}° {'N' if lat >= 0 else 'S'}"
                        lon_str = f"{abs(lon):.2f}° {'E' if lon >= 0 else 'W'}"
                        
                        # Generate the Google Maps URL
                        map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                        
                        print(f"{BOLD}\n[+] EARTH OBSERVATION ----------------------{RESET}{GREEN}")
                        print(f"    Sub-Planetary Point: {lat_str}, {lon_str}")
                        print(f"    Status: Visible above linked region.")
                        print(f"    Linked Region: {map_url}{RESET}")
            
            # Keep prompt green
            raw_prompt = input(f"{GREEN}\n> View raw data dump from NASA JPL Horizons? (y/n): {RESET}").strip().lower()
            if raw_prompt == 'y':
                print(f"{GREEN}{raw_result}{RESET}")
        else:
            print(f"{GREEN}Error: Could not find ephemeris data in the response.{RESET}")
    else:
        print(f"{GREEN}Error: {response.status_code}{RESET}")

if __name__ == "__main__":
    while True:
        # Clear screen at start of every loop
        clear_screen()
        # Print ASCII header
        print_header()
        
        # Retro formatting to the input prompt
        userEntry = input(f"{GREEN}> Enter a solar planet (or 'quit'): {RESET}").strip().lower()

        if userEntry in ["quit", "exit", "q"]:
            print(f"{GREEN}> Terminating connection...{RESET}")
            break

        if userEntry in PLANET_IDS:
            target_id = PLANET_IDS[userEntry]
            print(f"{GREEN}> Uplink established. Requesting NASA telemetry for {userEntry.capitalize()} (ID: {target_id})...{RESET}")
            get_planet_data(target_id)
            
            # Pause before looping so screen doesnt clear instantly
            input(f"{GREEN}\n> Press Enter to continue...{RESET}")
        
        else:
            print(f"{GREEN}> Planetary body not found in database.{RESET}")
            input(f"{GREEN}\n> Press Enter to continue...{RESET}")