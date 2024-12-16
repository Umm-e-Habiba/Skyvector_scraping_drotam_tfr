import requests
import json
import csv
import re
from itertools import product
import random
import time
def generate_grid(bounds, grid_size=2):
    """
    Generate a grid of coordinates within the given bounds.
    Args:
        bounds: tuple of (min_lat, max_lat, min_lon, max_lon)
        grid_size: size of each grid cell in degrees
    Returns:
        List of coordinate boxes (ll1_lat, ll1_lon, ll2_lat, ll2_lon)
    """
    min_lat, max_lat, min_lon, max_lon = bounds
    # Generate latitude and longitude ranges
    lat_ranges = list(range(int(min_lat), int(max_lat), grid_size))
    lon_ranges = list(range(int(min_lon), int(max_lon), grid_size))
    grid_boxes = []
    for lat in lat_ranges:
        for lon in lon_ranges:
            box = (
                lat,  # ll1_lat
                lon,  # ll1_lon
                min(lat + grid_size, max_lat),  # ll2_lat
                min(lon + grid_size, max_lon)   # ll2_lon
            )
            grid_boxes.append(box)
    return grid_boxes
def make_api_request(box):
    """
    Make API request for a specific coordinate box
    """
    ll1_lat, ll1_lon, ll2_lat, ll2_lon = box
    center_lat = (ll1_lat + ll2_lat) / 2
    center_lon = (ll1_lon + ll2_lon) / 2
    url = (
        f"https://skyvector.com/api/dLayer?"
        f"ll={center_lat}%2C{center_lon}&"
        f"ll1={ll1_lat}%2C{ll1_lon}&"
        f"ll2={ll2_lat}%2C{ll2_lon}&"
        f"pv=0&res=2038.321&windMB=300&"
        f"windZulu=1734112800&layers=drotam&"
        f"rand={random.randint(0, 99999):05d}"
    )
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    }
    return requests.get(url, headers=headers)
def process_response(response, writer):
    """
    Process API response and write to CSV
    """
    if response.status_code != 200:
        print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
        return
    data = response.json()
    lat_lon_pattern = r'(\d{2})(\d{2})(\d{2})([N])(\d{3})(\d{2})(\d{2})([W])'
    for item in data.get('shapes', []):
        latitude = longitude = None
        if 'txt' in item:
            lat_lon_match = re.search(lat_lon_pattern, item['txt'])
            if lat_lon_match:
                lat_deg, lat_min, lat_sec, lat_dir, lon_deg, lon_min, lon_sec, lon_dir = lat_lon_match.groups()
                latitude = int(lat_deg) + int(lat_min) / 60 + int(lat_sec) / 3600
                longitude = int(lon_deg) + int(lon_min) / 60 + int(lon_sec) / 3600
                if lon_dir == 'W':
                    longitude = -longitude
        row = [
            item.get('a2', ''),
            item.get('a1', ''),
            item.get('txt', ''),
            item.get('t', ''),
            item.get('id', ''),
            item.get('fs', ''),
            item.get('n', ''),
            item.get('ts', ''),
            item.get('v', ''),
            latitude,
            longitude
        ]
        writer.writerow(row)
def main():
    # Define search areas (from your original URLs)
    search_areas = [
        #(53.54901, 59.27898, -144.40796, -124.08325),  # Alaska region
        (21.58253, 53.54466, -146.90186, -65.60303)   # Continental US
        #(20.05894, 22.47745, -160.63568, -155.55450),  # Hawaii
        #(7.07037, 19.17838, 132.16333, 156.55298),     # Guam region
        #(53.52725, 68.33843, -172.22168, -111.24756)   # Alaska extended
    ]
    with open("API_data_grid.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['a2', 'a1', 'txt', 't', 'id', 'fs', 'n', 'ts', 'v', 'coordinate_x', 'coordinate_y']
        writer.writerow(header)
        for area in search_areas:
            print(f"\nProcessing area: {area}")
            grid_boxes = generate_grid(area, grid_size=2)  # 2-degree grid size
            for box in grid_boxes:
                print(f"Processing box: {box}")
                response = make_api_request(box)
                process_response(response, writer)
                time.sleep(1)  # Add delay between requests to avoid rate limiting
if __name__ == "__main__":
    main()