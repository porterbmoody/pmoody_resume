#%%
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd
from termcolor import colored
from datetime import date
from tqdm import tqdm

break_ = colored("---------------------------------------------------------------------", 'green')

def open_driver(driver_path):
    """ Opens drivers to specific url and grabs soup
    """
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path = driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    return driver

def login(driver):
    username = "7193385009"
    password = "Yoho1mes"
    time.sleep(1)
    # login
    login = 'n'
    driver.find_element('name', 'email').send_keys(username)
    driver.find_element('name',  'pass').send_keys(password)
    time.sleep(2)
    # find the login button by its aria-label attribute
    login_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Accessible login button']")
    # click the login button
    login_button.click()
    time.sleep(1)
    print(colored("LOGIN SUCCESSFUL", "green"))

def scroll_down(driver, number_of_scrolls):
    print(colored("\nscrolling on: " + driver.current_url, 'green'))
    # print(colored("iteration: " + str(iteration + 1), 'blue'))
    for scroll in tqdm(range(number_of_scrolls)):

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(.7)

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

def scrape(driver, search_item, search_location, search_location_code, path, number_of_scrolls):
    print(break_)
    print("searching for: " + search_item)
    print("location: ", search_location)
    url = 'https://www.facebook.com/marketplace/' + search_location_code + '/' + search_item

    # open driver and get soup
    print("\nOpening driver...")
    driver.get(url)
    scroll_down(driver, number_of_scrolls)

    soup             = BeautifulSoup(driver.page_source, 'html.parser')
    new_data         = extract_data_from_soup(soup)
    new_data = new_data.dropna(subset=['title'])
    new_data = new_data[~new_data['title'].str.contains('hot wheel|toy|disney|hotwheels|Pixar|Fast And Furious', case=False)]
    new_locations = new_data.groupby('location').count().reset_index()

    # remove old car rows lol
    old_data         = pd.read_csv(path)
    data, duplicates = merge_data(new_data, old_data, duplicate_columns=['title','mileage','price','location'])
    # results
    old_data_length = len(old_data)
    data_length = len(data)
    print(data)
    change = data_length - old_data_length
    print(colored("rows extracted from web page: " + str(len(new_data)), 'yellow'))
    print(colored("duplicate rows detected: " + str(duplicates), 'red'))
    print(colored("net rows added: "          + str(change), 'green'))
    print(colored("location(s): " , 'magenta'))
    print(colored(new_locations[['location', 'title']].sort_values(by='title', ascending=False), 'magenta'))
    print(break_)
    print(colored('\ntotal rows: '+ str(data_length)+'\n', 'green'))

    if change != 0:
        data.to_csv(path, index = False)

def main():
    # declare path variables
    driver_path     = r'./Facebook Marketplace Project/chromedriver.exe'
    data_cities     = './Facebook Marketplace Project/data/data_cities.csv'
    path            = './Facebook Marketplace Project/data/cars_total.csv'
    # path_today      = './Facebook Marketplace Project/data/cars_total_' + str(date.today()) + '.csv'
    url             = 'https://www.facebook.com/marketplace/phoenix/cars'

    data_cities = pd.read_csv(data_cities)
    driver = open_driver(driver_path)
    driver.get(url)
    login(driver)

    data_cities = data_cities
    for index, row in data_cities.iterrows():
        row = list(row)
        search_location      = row[0]
        search_location_code = row[1]
        search_item          = "cars"
        scrape(driver, search_item, search_location, search_location_code, path, 10)

    driver.minimize_window()
    driver.close()
    driver.quit()

if __name__ == "__main__":
    start_time = time.time()
    main()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Elapsed time: {:.2f} seconds".format(elapsed_time))


# git add .
# git commit -m "awesomeness"
# git push
