#%%

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

class Bot:
    def __init__(self) -> None:
        self.message_template = 'Hey,\n\nOur message is short. We will double your ad spend ROI within a couple months, and if we don’t then our service is free.\n\nNo more monthly subscriptions, no more marketing companies not getting the returns that you wanted. \n\nWe get you what you want, or it’s free. That simple. \n\nWe average a 2x-4x ROI, and we will get that for you. \n\nMessage me back and we can get on a call to talk about the details.\n\nTalk to you soon,\n\nGarret - Founder of Page One Marketing'
        self.subject = 'Double Your ROI or Our Service is Free – No Risk, All Reward'
        self.data = pd.read_csv('data.csv')

    def open_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://mail.google.com/')
        time.sleep(5)

    def send_emails(self):
        for index, row in self.data.iterrows():
            to_email = row['to_emails']
            status = row['status']
            print(to_email, status)
            if status == 'unsent':
                compose_button = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="T-I T-I-KE L3"]')))
                compose_button.click()
                to_box = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="To recipients"]')))
                to_box.send_keys(to_email)
                subject_box = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="subjectbox"]')))
                subject_box.send_keys(self.subject)
                # input('next')
                message_body_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Message Body"]')))
                # message_body_input.send_keys(self.message_template)
                bot.driver.execute_script("arguments[0].value = 'Hello, World!';", message_body_input)
                # self.driver.execute_script("arguments[0].value = arguments[1];", message_body_input, self.message_template)
                send_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="button"]')))
                send_button.click()
                self.data.at[index, 'status'] = 'sent'
                input('done?')

            self.data.to_csv('data.csv', index = False)

    def run(self):
        self.open_browser()
        username_box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="email"]')))
        username_box.send_keys('portersspotify@gmail.com')
        next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b"]')))
        next_button.click()
        # password_box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="password"]')))
        # password_box.send_keys('Yoho1mes')
        # next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b"]')))
        # next_button.click()
        input('ready?')
        self.send_emails()

bot = Bot()

bot.run()

#%%
message_body_input = bot.driver.find_element(By.CSS_SELECTOR, '[aria-label="Message Body"]')
message_body_input
bot.driver.execute_script("arguments[0].click();", message_body_input)



#%%
bot.driver.execute_script("arguments[0].innerHTML  = 'Hello, World!';", message_body_input)

# %%

bot.driver.execute_script("""
    var div = arguments[0];
    var textNode = document.createTextNode('Hello, ');
    var strongNode = document.createElement('strong');
    strongNode.textContent = 'World!';
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
    div.appendChild(textNode);
    div.appendChild(strongNode);
""", message_body_input)
