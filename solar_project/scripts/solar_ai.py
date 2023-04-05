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

static_map_url = f'https://maps.googleapis.com/maps/api/staticmap?center={address}&zoom={zoom}&size={size}&maptype={maptype}&key={static_map_key}'
print(static_map_url)

response = requests.get(static_map_url, stream=True)

with open('sav.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

# del response

#%%
# def address_to_long_lat(address, geocoding_key):
#     geo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, geocoding_key)
#     print(geo_url)
#     response = requests.get(geo_url)
#     results = response.json()['results']
#     print(results)
#     my_geo = results[0]['geometry']['location']
#     long, lat = my_geo['lng'], my_geo['lat']
#     print("lat:",lat, "long:", long)
#     return long, lat




# geocoding_key = 'AIzaSyDqmrxYDo6AhcB803AImc6zFRTPBI9r7gk'
# long, lat = address_to_long_lat(address, geocoding_key)
# print(lat, long)







# if __name__ == "__main()__":
    # main()
# main()




#%%

url = 'https://maps.googleapis.com/maps/api/staticmap?center=colorado springs, co&zoom=14&size=400x400&key=AIzaSyBYZHD0dhidkig5nUiiCaDC6dDlEHiCzy8'
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path = driver_path, options=options)
input("enter:")
driver.get(url)



#%%
