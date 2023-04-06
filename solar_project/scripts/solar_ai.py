#%%
from datetime import datetime
import requests
from selenium import webdriver
import shutil
import pandas as pd

# Read the CSV file
addresses_master_list = '../data/master-address-list.csv'
addresses_manual_list = '../data/addresses.csv'
data = pd.read_csv(addresses_manual_list, sep = '\t')
# data.to_csv(addresses_manual_list, index=False)

addresses = list(data['address'])
print(addresses)

#%%

def get_geocoding(address):
    geocoding_key = 'AIzaSyDqmrxYDo6AhcB803AImc6zFRTPBI9r7gk'
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={geocoding_key}'
    response = requests.get(geocoding_url)
    return response['results'][0]

def get_static_image(address):
    driver_path = 'D:/Desktop/School/pmoody_resume/Facebook Marketplace Project/chromedriver.exe'

    zoom = '20'
    size = '400x400'
    maptype = 'satellite'
    static_map_key = 'AIzaSyBYZHD0dhidkig5nUiiCaDC6dDlEHiCzy8'

    static_map_url = f'https://maps.googleapis.com/maps/api/staticmap?center={address}&zoom={zoom}&size={size}&maptype={maptype}&key={static_map_key}'
    # print(static_map_url)
    # print("getting static image for:", address)
    response = requests.get(static_map_url, stream=True)

    return response.raw


address = addresses[0]
# for address in addresses[5:]:
print("address:", address)
print("getting geocoding...")
response = get_geocoding(address)

lat = response['geometry']['location']['lat']
lng = response['geometry']['location']['lng']
plus_code = response['plus_code']['global_code']
formatted_address = response['formatted_address']

print("Latitude:", lat)
print("Longitude:", lng)
print("Plus Code:", plus_code)
print("Formatted Address:", formatted_address)
print("plus code:", plus_code)

image_raw = get_static_image(address)
with open('../data/images_without_panels/' + address + '.png', 'wb') as out_file:
    shutil.copyfileobj(image_raw, out_file)



#%%



# git add .
# git commit -m "solar ai"
# git push