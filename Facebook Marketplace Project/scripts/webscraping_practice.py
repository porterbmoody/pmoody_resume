#%%

from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver_path     = r'./Facebook Marketplace Project/chromedriver.exe'
data_cities     = './Facebook Marketplace Project/data/data_cities.csv'
path            = '../../Facebook Marketplace Project/data/cars_total.csv'
# path_today      = './Facebook Marketplace Project/data/cars_total_' + str(date.today()) + '.csv'
url             = 'https://www.facebook.com/marketplace/phoenix/cars'

data = pd.read_csv(path).tail(10)
print(data)

def open_driver(driver_path):
    """ Opens drivers to specific url and grabs soup
    """
    chrome_options = uc.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = uc.Chrome(executable_path = driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    return driver

#%%
driver = open_driver(driver_path)
driver.get('https://accounts.google.com/servicelogin')

#%%
# google username and password
username_form = driver.find_element(By.XPATH, '//input[@type="email"]')
username_form.send_keys('porterbmoody@gmail.com')
next_button = driver.find_element(By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]')
next_button.click()

#%%
password_form = driver.find_element(By.XPATH, '//input[@type="password"]')
password_form.send_keys('Yoho1mes')

next_button = driver.find_element(By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]')
next_button.click()



kbb_url = 'https://www.kbb.com/whats-my-car-worth/'
driver.get(kbb_url)
# select make/model



#%%
time.sleep(4)
option_to_click = driver.find_element(By.XPATH, "//div[contains(text(),'Make/Model')]")
option_to_click.click()

from selenium.webdriver.support.ui import Select
year_dropdown = Select(driver.find_element(By.XPATH, '//select[@aria-label="Year"]'))
year_dropdown.select_by_value('2011')

#%%

driver.close()
driver.quit()


# %%
