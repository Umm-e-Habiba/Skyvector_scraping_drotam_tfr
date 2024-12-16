import requests
import json
import csv
import re

# Step 1: Set the API URL
url = "https://skyvector.com/api/dLayer?ll=35.24562%2C-97.97168&ll1=12.68322%2C-152.37597&ll2=52.93540%2C-43.56738&pv=0&res=9783.940&windMB=300&windZulu=1734123600&layers=tfr&rand=14553"  # Replace with the actual API URL

# Step 2: Set any necessary headers or parameters (if required)
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Replace with your token if needed
}
# Open the file in write mode


# Step 3: Make a GET request to the API
response = requests.get(url, headers=headers)

# Step 4: Check if the request was successful
if response.status_code == 200:
    with open("API_data_TFR.csv", "w", newline="") as file:
        writer = csv.writer(file)
        header = ['a2', 'a1', 't', 'id', 'fs', 'n', 'ts', 'v','u', 'r']
        writer.writerow(header)
        # Parse the JSON response
        data = response.json()  # This will convert the response into a Python dictionary
        #print(json.dumps(data, indent=4))  # Print the data nicely formatted
        a1 = None
        a2 = None
        t= None
        id= None
        fs= None
        n= None
        ts= None
        v= None
        u=None
        r=None
        
        
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
            if 'r' in item:
                r = item['r']
                print("\nr:",r)
            if 'u' in item:
                u = item['u']
                print("\nu:",u)
                
            
            row = [item.get('a2', ''), item.get('a1', ''), item.get('txt', ''), item.get('t', ''),
                item.get('id', ''), item.get('fs', ''), item.get('n', ''), item.get('ts', ''), item.get('v', ''),item.get('u', ''),item.get('r', ''),]
            writer.writerow(row)
        print("\nData has been successfully written to API_data_TFR.csv.")
    
else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")

