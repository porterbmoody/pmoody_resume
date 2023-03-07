#%%
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import pandas as pd
from termcolor import colored
from datetime import date
import os
from time import sleep
from tqdm import tqdm

# pd.set_option("display.max_rows", 120)
# pd.set_option('display.max_colwidth', -1)
break_ = colored("---------------------------------------------------------------------", 'yellow')

def open_driver(url, driver_path):
    """ Opens drivers to specific url and grabs soup
    """
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path = driver_path, chrome_options=chrome_options)
    driver.manage().window().maximize()
    return driver

def scroll_down(driver, iterations):
    print(colored("\nscrolling... ", 'green'))
    # print(colored("iteration: " + str(iteration + 1), 'blue'))
    for iteration in tqdm(range(10)):
        scroll_pause_time = 1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(random.randint(350,650)/100)

def extract_data_from_soup(soup):
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
            'date_scraped' : date.today()
            }))
    return data

def merge_data(new_data, old_data, duplicate_columns):
    """ Join newly scraped data with stored data
    """
    # join new data with old
    data = pd.concat([old_data, new_data], ignore_index=True)
    data_before_dropping_duplicates_length = len(data)
    data = data.drop_duplicates(subset = duplicate_columns, keep='last')
    data_after_dropping_duplicates_length = len(data)
    duplicates = data_before_dropping_duplicates_length - data_after_dropping_duplicates_length
    return data, duplicates

def main():
    # declare path variables
    driver_path     = r'./Facebook Marketplace Project/chromedriver.exe'
    data_cities     = './Facebook Marketplace Project/data/data_cities.csv'
    path            = './Facebook Marketplace Project/data/cars_total.csv'
    path_today      = './Facebook Marketplace Project/data/cars_total_' + str(date.today()) + '.csv'

    data_cities = pd.read_csv(data_cities)
    driver = open_driver(url, driver_path)
    login = 'n'

    for index, row in data_cities.head(1).iterrows():
        row = list(row)
        search_location      = row[0]
        search_location_code = row[1]
        search_item          = "cars"

        print(break_)
        print("searching for: " + search_item)
        print("location: ", search_location)
        url = 'https://www.facebook.com/marketplace/' + search_location_code + '/' + search_item

        # open driver and get soup
        print("\nOpening driver...")
        driver.get(url)

        # time.sleep(random.randint(100,2000)/100)
        if login != "y":
            login = input("Are you logged in? (y/n)\n")

        scroll_down(driver, 3)

        soup             = BeautifulSoup(driver.page_source, 'html.parser')
        new_data         = extract_data_from_soup(soup)
        new_data = new_data.dropna(subset=['title'])
        new_data = new_data[~new_data['title'].str.contains('hot wheel|toy|disney|hotwheels|Pixar|Fast And Furious', case=False)]
        # remove to car rows lol
        old_data         = pd.read_csv(path)
        data, duplicates = merge_data(new_data, old_data, duplicate_columns=['title','mileage','price','location'])
        # results
        old_data_length = len(old_data)
        data_length = len(data)
        print(data)
        change = data_length - old_data_length
        print(colored("rows extracted from web page: "          + str(len(new_data)), 'yellow'))
        print(colored("duplicate rows detected: " + str(duplicates), 'red'))
        print(colored("net rows added: "          + str(change), 'green'))
        print(colored("location(s): " + search_location, 'magenta'))
        print(break_)
        print(colored('\ntotal rows: '+ str(data_length)+'\n', 'green'))

        if change != 0:
            data.to_csv(path, index = False)
            # if os.path.exists(path):
                # data.to_csv(path_today, index = False)
    driver.minimize_window()
    driver.close()
    driver.quit()
    
    # data_cities.to_csv(path_cities, index=False)
    # data_cities = pd.read_csv(path)
    # search_location = list(cities_dict.keys())[4]
    # search_location = "denver"



if __name__ == "__main__":
    main()
    
    # wait_time = random.randint(0, 300*60)/99
    # print('Waiting:', round(wait_time), "seconds,",round(wait_time/60),"mins to run again.")


# git add .
# git commit -m "awesomeness"
# git push

# path            = 'C:/Users/porte/Desktop/coding/pmoody_resume/Facebook Marketplace Project/data/cars.csv'
# data = pd.read_csv(path)

# data_before_dropping_duplicates_length = len(data)
# data = data.drop_duplicates(subset = ['title','mileage','location'], keep='last')
# data_after_dropping_duplicates_length = len(data)
# duplicates = data_before_dropping_duplicates_length - data_after_dropping_duplicates_length

# print(duplicates)
# print(data[data.duplicated(['title', 'mileage', 'location'], keep=False)])


# def login(driver):
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     username = "7193385009"
#     password = "Yoho1mes"


#     # try:
#     #     driver.find_element_by_class_name(class_name).click()
#     # except:
#     #     print("No Click.")
#     time.sleep(3)
#     login_button = soup.find('div', {'aria-label':'Accessible login button'})
#     login_button.click()
#     time.sleep(3)

#     username = soup.find('input' , {'name':"email"})
#     password = soup.find('input' , {'name':"pass"})
#     # password = soup.find_element_by_id("pass")
#     # submit   = soup.find_element_by_id("loginbutton")
#     username.send_keys(username)
#     password.send_keys(password)
#     time.sleep(3)

#     submit = soup.find('button' , {'name' : 'login'})
#     submit.click()
#     time.sleep(3)
#     return driver


#%%
# import pandas as pd

# data = pd.read_csv('../data/cars_total.csv')

# # Drop rows that contain "hot wheel", "toy", "disney" somewhere in the cell of the column title
# data = data.dropna(subset=['title'])
# data = data[~data['title'].str.contains('hot wheel|toy|disney', case=False)]

# # filtered_data.to_csv('../data/doodoo_trash.csv')
# data.to_csv('../data/cars_total.csv', index=False)
