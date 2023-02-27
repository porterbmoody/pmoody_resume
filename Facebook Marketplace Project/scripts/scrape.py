#%%
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import pandas as pd
import re
from selenium.webdriver.chrome.options import Options
import numpy as np
from termcolor import colored
# import connect_to_mysql
from datetime import datetime
from datetime import date

# pd.set_option("display.max_rows", 120)
# pd.set_option('display.max_colwidth', -1)



break_ = colored("---------------------------------------------------------------------", 'yellow')
# %%
username = "porterbmoody@gmail.com"
password = "Yoho1mes"
# password = str(input("Enter password: "))

def open_driver(url, driver_path):
    """ returns soup
    """
    global driver
    driver = webdriver.Chrome(executable_path = driver_path)
    driver.get(url)
    # time.sleep(random.randint(100,2000)/100)

    input("Press Enter to close")

    # try:
    #     driver.find_element_by_class_name(class_name).click()
    # except:
    #     print("No Click.")
    ################## scrolling randomly
    scroll_down()
    scroll_down()
    scroll_down()
    driver.minimize_window()
    
    return driver

def extract_data(soup):
    """
    Input soup and this will extract data and return pandas dataframe
    """
    prices            = []
    titles            = []
    locations         = []
    mileages          = []
    links             = []

    listings_class            = 'x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6'
    title_class               = 'x1lliihq x6ikm8r x10wlt62 x1n2onr6'
    price_class               = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u'
    location_class            = 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84'
    mileage_class             = 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84'
    link_class                = 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv'

    listings              = soup.find_all('div', {"class" : listings_class})

    for listing in listings:
        title     = listing.find_all(class_ = title_class)
        price     = listing.find_all(class_ = price_class)
        mileage   = listing.find_all(class_ = mileage_class)
        location  = listing.find_all(class_ = location_class)
        link      = listing.find_all(class_ = link_class)
        
        if len(listing.find_all(class_ = price_class)) > 0:
            if len(title) > 0:
                title    = title[0].text
            else:
                title    = None
            price    = price[0].text
            if len(mileage) > 1:
                mileage  = mileage[1].text
            else:
                mileage = None
            if len(location) > 0:
                location = location[0].text
            else:
                location = None
            if len(link) > 0:
                link = "www.facebook.com" + link[0]['href']
            else:
                link = None

            titles.append(title)
            prices.append(price)
            mileages.append(mileage)
            locations.append(location)
            links.append(link)
            
    data = (pd.DataFrame({
            "title"        : titles,
            "mileage"      : mileages,
            "price"        : prices,
            "location"     : locations,
            'link'         : links,
            'date_scraped' : date.today()}))
    return data

def scroll_down():
    print(break_)
    print(colored("Scrolling...", 'yellow'))
    SCROLL_PAUSE_TIME = 0.7

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(random.randint(350,650)/100)

# def keep_open():
    
#     # time.sleep(5)

cities = {'colorado springs' : 'coloradosprings',
          'rexburg'          : '109379399080927',
          'phoenix'          : 'phoenix',
          'san francisco'    : 'sanfrancisco',
          'american falls idaho' : '107321972630622',
          'san diego'        : 'sandiego',
          'los angeles'      : 'la',
          'miami'            : 'miami',
          'charlotte'        : 'charlotte',
          'raleigh'          : 'raleigh',
          'provo'            : '106066949424984',
          'denver'           : 'denver',
          'new york'         : 'nyc',
          'chicago'          : 'chicago',
          'houston'          : 'houston',
          'philadelphia, PA' : 'philly',
          'san antonio'      : 'sanantonio',
          'dallas'           : 'dallas',
          'la paz'           : '104001876301959',
          'austin' : 'austin',
          'jacksonville' : '111879628828536',
          'hattiesburg' : '108528479168913'}

def main():
    # set paths and other variables
    driver_path = r'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/chromedriver.exe'
    path = 'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars.csv'
    # search_location = list(cities.keys())[-1]
    search_location = "phoenix"
    search_item     = "cars"
    url = "https://www.facebook.com/marketplace/" + cities[search_location] + "/search/?query=" + search_item

    # open driver and get soup
    print("\nOpening driver...")
    # driver = open_driver(url, driver_path)
    # soup = BeautifulSoup(driver.page_source, 'html.parser')

    # extract data
    new_data = pd.DataFrame()
    # new_data = extract_data(soup)

    # join new data with old
    old_data = pd.read_csv(path)
    data = pd.concat([old_data, new_data], ignore_index=True)
    data = data.drop_duplicates(subset = ['link'])

    #################################### results
    print(data)
    new_data_length = len(new_data)
    new_rows_added = len(data) - len(old_data)
    # print(colored("rows extracted: "         + str(len(new_data)), 'yellow'))
    print(colored("new rows added: "         + str(new_rows_added), 'green'))
    print(colored("duplicate rows detected: "+ str(new_data_length - new_rows_added), 'red'))
    print("location:", search_location)

    if new_rows_added > 0:
        data.to_csv(path, index = False)    

    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()
    
    # wait_time = random.randint(0, 300*60)/99
    # print('Waiting:', round(wait_time), "seconds,",round(wait_time/60),"mins to run again.")


# git add .
# git commit -m "awesomeness"
# git push