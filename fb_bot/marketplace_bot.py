#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re


pd.set_option('display.max_colwidth', None)

class Bot:

    def __init__(self) -> None:
        path = 'tradein_data.csv'
        self.tradein_data = pd.read_csv(path)
        self.urls = [
            "https://www.facebook.com/",
            "https://www.facebook.com/marketplace/coloradosprings/search/?query=iphone",
            ]
        self.listings_path = 'listings.csv'
        self.email = "porterbmoody@gmail.com"
        self.password = "Yoho1mes"

    def login_facebook(self):
        time.sleep(5)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.urls[0])
        email_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "email")))
        email_input.send_keys(self.email)
        password_input = self.driver.find_element(By.ID, "pass")
        password_input.send_keys(self.password)
        login_button = self.driver.find_element(By.NAME, "login")
        login_button.click()

    def scrape_iphone_listings(self):
        time.sleep(4)
        self.driver.get(self.urls[1])
        time.sleep(4)

        for _ in range(50):
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)
        locators = [
            "[class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv']",
            "[class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']",
            "[class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1jchvi3 x1lbecb7 x1s688f xzsf02u']",
            "[class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84']"
            # "[class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv']",
        ]
        items = self.driver.find_elements(By.CSS_SELECTOR, locators[0])
        results = []

        for item in items:
            title = item.find_element(By.CSS_SELECTOR, locators[1]).text
            price = item.find_element(By.CSS_SELECTOR, locators[2]).text
            price = self.convert_price(price)
            url = item.get_attribute('href')
            location = item.find_element(By.CSS_SELECTOR, locators[3]).text
            print(title, price, url, location)
            if location != 'Ships to you':
                results.append({'title': title, 'price': price, 'url' : url, 'location' : location})
        self.listings = pd.DataFrame(results)
        self.listings.to_csv(self.listings_path, index = False)

    @staticmethod
    def convert_price(price_str):
        """Convert price string to float after removing non-numeric characters."""
        price_str = re.sub(r'[^\d.]', '', price_str)
        try:
            return float(price_str)
        except ValueError:
            return None

    def find_deals(self):
        deals_found = []
        for i, listing in self.listings.iterrows():
            listing_title = listing['title']
            listing_price = listing['price']
            listing_url = listing['url']
            location = listing['location']

            for j, deal in self.tradein_data.iterrows():
                tradein_title = deal['device']
                tradein_value = deal['value']

                # Use regex to search for deal title within listing title
                if re.search(re.escape(tradein_title), listing_title, re.IGNORECASE):
                    # if listing_price > deal_price:  # or any other condition to determine a deal
                    deals_found.append({
                        'listing_title': listing_title,
                        'tradein_title': tradein_title,
                        'listing_price': listing_price,
                        'tradein_value': tradein_value,
                        'difference' : tradein_value - listing_price,
                        'location' : location,
                        'url' : listing_url,
                    })
        self.deals_found = pd.DataFrame(deals_found)
        self.deals_found = self.deals_found.sort_values(by = 'difference')
        self.deals_found.to_csv('deals_found.csv', index=False)

    def run_bot(self):
        self.login_facebook()
        self.scrape_iphone_listings()
        # self.listings = pd.read_csv(self.listings_path)
        self.find_deals()

# bot = Bot()
# bot.run_bot()

#%%

path = 'deals_found.csv'

deals = pd.read_csv(path)
deals.sort_values(by='difference', ascending=False).head(20)

#%%






