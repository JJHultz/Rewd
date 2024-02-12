#Rewd.py iteration 1
#Jace Hultzen copiloted by GPT-4

import requests
from datetime import datetime, timedelta
import pandas as pd
import json
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='')

# Meteomatics API credentials
username = 'test'
password = ''

# Time range for the API request
start_time = datetime.utcnow().isoformat() + "Z"  # Start time (now)
end_time = (datetime.utcnow() + timedelta(hours=48)).isoformat() + "Z"  # End time (48 hours from now)



# Location (latitude and longitude) and parameter of interest
while True:
    user_input = input("Enter a Location or Latitude")
    try:
        latitude = float(user_input)
        longitude = input("Enter Longitude or city")
        break
    except:
        #Geocoding
        geocode_result = gmaps.geocode(user_input)
        break

latitude = geocode_result[0]['geometry']['location']['lat']
longitude = geocode_result[0]['geometry']['location']['lng']


parameter = 'precip_1h:mm'  # Precipitation over 1 hour in mm

# Construct the API request URL
request_url = f"https://api.meteomatics.com/{start_time}--{end_time}:PT1H/{parameter}/{latitude},{longitude}/json"

# Make the API request with authentication
response = requests.get(request_url, auth=(username, password))

# Check if the request was successful
if response.status_code == 200:
    # Decode the response to JSON
    data = response.json()
    #print('Weather Data')
    #print(data)
else:
    print(f"Failed to retrieve data: {response.status_code} - {response.text}")

# Assuming `data` is your JSON response from the API
precip_data = data['data'][0]['coordinates'][0]['dates']

# Extracting date and value pairs
dates = [entry['date'] for entry in precip_data]
values = [entry['value'] for entry in precip_data]

# Creating a DataFrame
df = pd.DataFrame({'Date': dates, 'Precipitation (mm)': values})

# Converting 'Date' to datetime in UTC
df['Date'] = pd.to_datetime(df['Date'], utc=True)

# Convert 'Date' from UTC to Pacific Standard Time (PST)
df['Date'] = df['Date'].dt.tz_convert('America/Los_Angeles')

# Setting 'Date' as index
df.set_index('Date', inplace=True)

# Show the DataFrame
print(df)