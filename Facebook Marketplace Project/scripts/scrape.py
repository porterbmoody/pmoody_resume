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

# password = str(input("Enter password: "))

def open_driver(url, driver_path):
    """ returns soup
    """
    global driver
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path = driver_path, chrome_options=chrome_options)
    driver.get(url)

    # time.sleep(random.randint(100,2000)/100)
    input("Press Enter to continue\n")

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

def login(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    username = "7193385009"
    password = "Yoho1mes"

    time.sleep(3)
    login_button = soup.find('div', {'aria-label':'Accessible login button'})
    login_button.click()
    time.sleep(3)

    username = soup.find('input' , {'name':"email"})
    password = soup.find('input' , {'name':"pass"})
    # password = soup.find_element_by_id("pass")
    # submit   = soup.find_element_by_id("loginbutton")
    username.send_keys(username)
    password.send_keys(password)
    time.sleep(3)

    submit = soup.find('button' , {'name' : 'login'})
    submit.click()
    time.sleep(3)
    return driver

def extract_data(soup):
    """
    Input soup and this will extract data and 
    returns: pandas dataframe
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

def scrape_webpage(url, driver_path):
    """ Open driver and pull soup. Returns beautiful soup object
    """
    # open driver and get soup
    print("\nOpening driver...")
    driver = open_driver(url, driver_path)
    # driver = login(driver)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return extract_data(soup)

def merge_data(new_data, old_data):
    """ Join newly scraped data with stored data
    """
    # join new data with old
    data = pd.concat([old_data, new_data], ignore_index=True)
    data_before_dropping_duplicates_length = len(data)
    data = data.drop_duplicates(subset = ['title','mileage','price','location'], keep='last')
    data_after_dropping_duplicates_length = len(data)
    duplicates = data_before_dropping_duplicates_length - data_after_dropping_duplicates_length
    return data, duplicates

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
          'austin'           : 'austin',
          'jacksonville'     : '111879628828536',
          'hattiesburg'      : '108528479168913',
          'tallahassee'      : '107903159238479',
          'idaho falls'      : '105590229473679',
          'portland, OR'     : 'portland'}

def main():
    # set paths and other variables
    driver_path     = r'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/chromedriver.exe'
    path            = 'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars.csv'
    search_location = list(cities.keys())[-1]
    # search_location = "denver"
    search_item     = "cars"
    url             = "https://www.facebook.com/marketplace/" + cities[search_location] + "/search/?query=" + search_item

    new_data         = scrape_webpage(url, driver_path)
    old_data         = pd.read_csv(path)
    data, duplicates = merge_data(new_data, old_data)

    # results
    old_data_length = len(old_data)
    data_length = len(data)
    print(data)
    change = data_length - old_data_length
    print(colored("rows extracted from web page: "          + str(len(new_data)), 'yellow'))
    print(colored("duplicate rows detected: " + str(duplicates), 'red'))
    print(colored("net rows added: "          + str(change), 'green'))
    print(colored("location: " + search_location, 'magenta'))

    if change != 0:
        data.to_csv(path, index = False)

    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()
    
    # wait_time = random.randint(0, 300*60)/99
    # print('Waiting:', round(wait_time), "seconds,",round(wait_time/60),"mins to run again.")


git add .
git commit -m "awesomeness"
git push

# path = 'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars.csv'
# old_data = pd.read_csv(path)

# print(len(old_data))
# old_data = old_data.drop_duplicates(subset = ['title','mileage','price','location'])
# print(len(old_data))



