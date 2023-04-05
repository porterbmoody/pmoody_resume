#%%
import googlemaps
from datetime import datetime
import requests
from selenium import webdriver
driver_path = 'D:/Desktop/School/pmoody_resume/Facebook Marketplace Project/chromedriver.exe'

def address_to_long_lat(address):

    # Define the address to geocode
    address = "1730 Alamosa Dr"

    # Define the API endpoint URL
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=YOUR_API_KEY"

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    # Extract the latitude and longitude coordinates
    long = data["results"][0]["geometry"]["location"]["lng"]
    lat = data["results"][0]["geometry"]["location"]["lat"]

    print(f"Latitude: {lat}, Longitude: {long}")

    return long, lat

def get_image_from_api(image_download_path, url):
    # url = 'https://maps.googleapis.com/maps/api/staticmap?center={}&zoom={}&size=400x400&maptype=roadmap&markers=color:red%7C&key=AIzaSyBYZHD0dhidkig5nUiiCaDC6dDlEHiCzy8'.format(40.714728, -73.998672, lat, lng)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    input("enter:")
    driver = webdriver.Chrome(options=options)
    input("enter:")
    driver.get(url)
    driver.save_screenshot(image_download_path)
    input("enter:")
    driver.quit()



def main():
    address = "1730 alamosa dr. colorado springs"
    long, lat = address_to_long_lat(address = address)
    zoom = 20   
    size = '400x400'
    api_key = 'AIzaSyBYZHD0dhidkig5nUiiCaDC6dDlEHiCzy8'
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={long},{lat}&zoom={zoom}&size={size}&key={api_key}"
    print(url)
    # image = get_image_from_api(image_download_path="swag.png", url=url)


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

