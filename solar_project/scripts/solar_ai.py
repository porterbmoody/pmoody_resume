#%%
import googlemaps
from datetime import datetime
import requests
from selenium import webdriver
import shutil
driver_path = 'D:/Desktop/School/pmoody_resume/Facebook Marketplace Project/chromedriver.exe'

address = "166 w 5 w apt d7 Rexburg Id 83440"
zoom = '18'
size = '400x400'
maptype = 'satellite'
static_map_key = 'AIzaSyBYZHD0dhidkig5nUiiCaDC6dDlEHiCzy8'
# geocoding_key = 'AIzaSyDqmrxYDo6AhcB803AImc6zFRTPBI9r7gk'

static_map_url = f'https://maps.googleapis.com/maps/api/staticmap?center={address}&zoom={zoom}&size={size}&maptype={maptype}&key={static_map_key}'
print(static_map_url)

response = requests.get(static_map_url, stream=True)

with open('sav.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

# del response


#%%
