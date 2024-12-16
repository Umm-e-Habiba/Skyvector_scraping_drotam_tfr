import requests
import csv
import re
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_grid(bounds, grid_size=1):
    """
    Generate a grid of coordinates within the given bounds.
    """
    min_lat, max_lat, min_lon, max_lon = bounds
    lat_ranges = list(range(int(min_lat), int(max_lat), grid_size))
    lon_ranges = list(range(int(min_lon), int(max_lon), grid_size))
    grid_boxes = [
        (lat, lon, min(lat + grid_size, max_lat), min(lon + grid_size, max_lon))
        for lat in lat_ranges for lon in lon_ranges
    ]
    return grid_boxes

def make_api_request(box):
    """
    Make API request for a specific coordinate box.
    """
    ll1_lat, ll1_lon, ll2_lat, ll2_lon = box
    center_lat = (ll1_lat + ll2_lat) / 2
    center_lon = (ll1_lon + ll2_lon) / 2
    url = (
        f"https://skyvector.com/api/dLayer?"
        f"ll={center_lat}%2C{center_lon}&"
        f"ll1={ll1_lat}%2C{ll1_lon}&"
        f"ll2={ll2_lat}%2C{ll2_lon}&"
        f"pv=0&res=250&windMB=300&"
        f"windZulu=1734112800&layers=drotam&"
        f"rand={random.randint(0, 99999):05d}"
    )
    headers = {
        'User-Agent': 'Mozilla/5.0',
        # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Uncomment if needed
    }
    response = requests.get(url, headers=headers, timeout=10)
    time.sleep(1) 
    return response, box

def process_response(response, writer):
    """
    Process API response and write to CSV.
    """
    if response.status_code != 200:
        print(f"Failed to retrieve data for box. HTTP Status Code: {response.status_code}")
        return
    data = response.json()
    lat_lon_pattern = r'(\d{2})(\d{2})(\d{2})([N|S])(\d{3})(\d{2})(\d{2})([E|W])'
    for item in data.get('shapes', []):
        latitude = longitude = None
        if 'txt' in item:
            lat_lon_match = re.search(lat_lon_pattern, item['txt'])
            if lat_lon_match:
                lat_deg, lat_min, lat_sec, lat_dir, lon_deg, lon_min, lon_sec, lon_dir = lat_lon_match.groups()
                latitude = int(lat_deg) + int(lat_min) / 60 + int(lat_sec) / 3600
                longitude = int(lon_deg) + int(lon_min) / 60 + int(lon_sec) / 3600
                if lat_dir == 'S':
                    latitude = -latitude
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
    search_areas = [
        (21.58253, 53.54466, -146.90186, -65.60303)  # Continental US
    ]
    with open("API_data_grid.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['a2', 'a1', 'txt', 't', 'id', 'fs', 'n', 'ts', 'v', 'coordinate_x', 'coordinate_y']
        writer.writerow(header)
        
        for area in search_areas:
            print(f"\nProcessing area: {area}")
            grid_boxes = generate_grid(area, grid_size=1)  # 2-degree grid size
            with ThreadPoolExecutor(max_workers=12) as executor:  # Adjust the number of workers as needed
                futures = {executor.submit(make_api_request, box): box for box in grid_boxes}
                for future in as_completed(futures):
                    response, box = future.result()
                    print(f"Processing completed for box: {box}")
                    process_response(response, writer)

if __name__ == "__main__":
    main()
