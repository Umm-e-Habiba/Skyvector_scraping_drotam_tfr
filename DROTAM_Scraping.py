import requests
import json
import csv
import re

# Step 1: Set the API URL
urls =[
"https://skyvector.com/api/dLayer?ll=56.52213%2C-134.24561&ll1=53.54901%2C-144.40796&ll2=59.27898%2C-124.08325&pv=0&res=2038.321&windMB=300&windZulu=1734112800&layers=drotam&rand=45908",
"https://skyvector.com/api/dLayer?ll=39.35695%2C-106.25244&ll1=21.58253%2C-146.90186&ll2=53.54466%2C-65.60303&pv=0&res=8153.283&windMB=300&windZulu=1734112800&layers=drotam&rand=04738", #
"https://skyvector.com/api/dLayer?ll=21.26975%2C-158.09875&ll1=20.05894%2C-160.63568&ll2=22.47745%2C-155.55450&pv=0&res=509.580&windMB=300&windZulu=1734112800&layers=drotam&rand=74781",#Replace with the actual API URL
"https://skyvector.com/api/dLayer?ll=13.19930%2C144.35815&ll1=7.07037%2C132.16333&ll2=19.17838%2C156.55298&pv=0&res=2445.985&windMB=300&windZulu=1734112800&layers=drotam&rand=79953",
"https://skyvector.com/api/dLayer?ll=61.81207%2C-141.73462&ll1=53.52725%2C-172.22168&ll2=68.33843%2C-111.24756&pv=0&res=6114.962&windMB=300&windZulu=1734112800&layers=drotam&rand=83047"

]

# Step 2: Set any necessary headers or parameters (if required)
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Replace with your token if needed
}
# Open the file in write mode
with open("API_data_Drotams.csv", "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ['a2', 'a1', 'txt', 't', 'id', 'fs', 'n', 'ts', 'v','coordinate_x', 'coordinate_y']
    writer.writerow(header)
    for url in urls:
        # Step 3: Make a GET request to the API
        response = requests.get(url, headers=headers)

        # Step 4: Check if the request was successful
        if response.status_code == 200:
            
                # Parse the JSON response
                data = response.json()  # This will convert the response into a Python dictionary
                #print(json.dumps(data, indent=4))  # Print the data nicely formatted
                a1 = None
                a2 = None
                txt= None
                t= None
                id= None
                fs= None
                n= None
                ts= None
                v= None
                latitude=None
                longitude=None
                lat_lon_pattern = r'(\d{2})(\d{2})(\d{2})([N])(\d{3})(\d{2})(\d{2})([W])' 
                
                for item in data['shapes']:
                    
                    if 'a2' in item:
                        a2 = item['a2']
                        print("\na2:",a2)
                    if 'a1' in item:
                        a1 = item['a1']
                        print("\na1:",a1)
                        
                    if 't' in item:
                        t = item['t']
                        print("\ntype:",t)
                    if 'id' in item:
                        id = item['id']
                        print("\nIdentifier:",id)
                    if 'fs' in item:
                        fs = item['fs']
                        print("\nNotam ID:",fs)
                    if 'n' in item:
                        n = item['n']
                        print("\nNOTAM Number:",n)
                    if 'ts' in item:
                        ts = item['ts']
                        print("\nExpiration Timestamp:",ts)
                    if 'v' in item:
                        v = item['v']
                        print("\nValidity Period:",v)
                    if 'txt' in item:
                        txt = item['txt']
                        print("\nText:",txt)
                        lat_lon_match = re.search(lat_lon_pattern, txt)
                        if lat_lon_match:
                            lat_deg, lat_min, lat_sec, lat_dir, lon_deg, lon_min, lon_sec, lon_dir = lat_lon_match.groups()
                            latitude = int(lat_deg) + int(lat_min) / 60 + int(lat_sec) / 3600
                            longitude = int(lon_deg) + int(lon_min) / 60 + int(lon_sec) / 3600
                            if lat_dir == 'S':
                                latitude = -latitude
                            print("\nLatitude:",latitude)
                            if lon_dir == 'W':
                                longitude = -longitude
                            print("\nLongitude:",longitude)
                        else:
                            latitude, longitude = None, None

                    
                    row = [item.get('a2', ''), item.get('a1', ''), item.get('txt', ''), item.get('t', ''),
                        item.get('id', ''), item.get('fs', ''), item.get('n', ''), item.get('ts', ''), item.get('v', ''),latitude,longitude]
                    writer.writerow(row)
                print("\nData has been successfully written to data.csv.")
            
        else:
            print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")

