#%%

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = "https://www.linkedin.com/"

driver = webdriver.Chrome()
driver.get(url)

phone = '7193385009'
password = 'Yoho1mes'

time.sleep(2)
#%%
username_class_name = '.text-color-text.font-sans.text-md.outline-0.bg-color-transparent.grow'
username_input_box = driver.find_elements(By.CSS_SELECTOR, username_class_name)
username_input_box[0].send_keys(phone)
username_input_box[1].send_keys(password)

time.sleep(2)
#%%
login_button = driver.find_element(By.CSS_SELECTOR, ".btn-md.btn-primary.flex-shrink-0.cursor-pointer")

login_button.click()
time.sleep(2)
#%%
driver.quit()

