#%%

import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui
import re

class Bot:

    def __init__(self) -> None:
        self.url = "https://www.linkedin.com/"
        self.phone = '7193385009'
        self.password = 'Yoho1mes'

        self.button_classes = {
            'username' : 'text-color-text font-sans text-md outline-0 bg-color-transparent grow',
            'login_button' : 'btn-md btn-primary flex-shrink-0 cursor-pointer',
            'top_buttons' : 't-12 break-words block t-black--light t-normal',
            'conversations' : 'msg-conversation-card msg-conversations-container__pillar',
            'recipients' : 'msg-conversation-listitem__participant-names msg-conversation-card__participant-names truncate pr1 t-16 t-black',
            'text_box' : 'msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 full-height notranslate',
            'send_message_button' : 'msg-form__send-button artdeco-button artdeco-button--1',
            'attachment_buttons' : 'msg-form__footer-action artdeco-button artdeco-button--tertiary artdeco-button--circle artdeco-button--muted m0 artdeco-button--2'
        }

        self.format_button_classes()

    def format_button_classes(self):
        for class_name, class_value in self.button_classes.items():
            updated_value = class_value.replace(' ', '.')
            self.button_classes[class_name] = '.' + updated_value

        print(self.button_classes)

    def load_browser(self):

        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
    
    def login(self):
        username_input_box = self.driver.find_elements(By.CSS_SELECTOR, self.button_classes['username'])
        username_input_box[0].send_keys(self.phone)
        username_input_box[1].send_keys(self.password)
        login_button = self.driver.find_element(By.CSS_SELECTOR, self.button_classes['login_button'])
        login_button.click()
        input('next: ')
        # time.sleep(14)

    def open_conversation(self):
        conversations_button = self.driver.find_elements(By.CSS_SELECTOR, self.button_classes['top_buttons'])[3]
        conversations_button.click()
        time.sleep(2)

        conversations = self.driver.find_elements(By.CSS_SELECTOR, self.button_classes['conversations'])
        recipients = self.driver.find_elements(By.CSS_SELECTOR, self.button_classes['recipients'])

        print(conversations)
        for index, recipient in enumerate(recipients):
            if re.search(r"Martin Vaughn", recipient.text):
                conversations[index].click()
                break

        time.sleep(2)

    def send_message(self, message):
        text_box = self.driver.find_element(By.CSS_SELECTOR, self.button_classes['text_box'])
        print(text_box.text)
        message = 'this is an automated message'
        text_box.send_keys(message)
        time.sleep(2)
        print('sending message...')
        send_button = self.driver.find_element(By.CSS_SELECTOR, self.button_classes['send_message_button'])
        send_button.click()

    def add_attachment(self):
        link_attachment_button = self.driver.find_element(By.CSS_SELECTOR, self.button_classes['attachment_buttons'])
        link_attachment_button.click()
        print('sending image')
        # link_attachment_button.send_keys(image_path)
        file_path = 'C:/Users/Captain/Pictures/guy_peeing.png'
        pyautogui.write(file_path)
        pyautogui.press('enter')

    def quit(self):
        self.driver.quit()

bot = Bot()

bot.load_browser()
bot.login()
bot.open_conversation()
message = 'this is an automated message'
bot.send_message(message)
bot.add_attachment()
# C:/Users/Captain/Pictures/guy_peeing.png/



#%%
bot.quit()


#%%

image_path = 'C:/Users/Captain/Pictures/guy_peeing.png'
button = bot.driver.find_element(By.CSS_SELECTOR, bot.button_classes['attachment_buttons'])
button.send_keys(image_path)


#%%
link_attachment_button = bot.driver.find_element(By.CSS_SELECTOR, bot.button_classes['attachment_buttons'])

link_attachment_button

#%%

file_path = 'C:/Users/Captain/Pictures/guy_peeing.png'
pyautogui.write(file_path)
pyautogui.press('enter')

#%%

import requests

# Define the proxy server
proxy = {
    'http': 'http://your_proxy_server:port',
    'https': 'http://your_proxy_server:port'
}

# Make a request through the proxy
response = requests.get('http://example.com', proxies=proxy)

# Print the response
print(response.text)


#%%

print("asdfasdf")

