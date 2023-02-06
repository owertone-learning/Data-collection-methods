from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
from pymongo import MongoClient

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)

driver.get('https://account.mail.ru/login')

wait = WebDriverWait(driver, 10)
login = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
login.send_keys("study.ai_172@mail.ru")
login.send_keys(Keys.ENTER)

wait = WebDriverWait(driver, 10)
pwd = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
pwd.send_keys("Password!@#")
pwd.send_keys(Keys.ENTER)

wait = WebDriverWait(driver, 10)
links = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="llc llc_normal llc_first llc_new llc_new-selection js-letter-list-item js-tooltip-direction_letter-bottom"]')))
links.click()

def get_mail(driver):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.msg_db
    db.msg_items
    db.msg_items.insert_one({
        'author': driver.find_element(By.CLASS_NAME, 'letter-contact').get_attribute('title'),
        'date': driver.find_element(By.CLASS_NAME, 'letter__date').text,
        'subject': driver.find_element(By.TAG_NAME, 'h2').text,
        'text': driver.find_element(By.CLASS_NAME, 'letter-body').text,
    })

while True:
    try:
        time.sleep(1)
        get_mail(driver)
        wait = WebDriverWait(driver, 20)
        print()
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@data-title-shortcut,"Ctrl+↓")]')))
        next_button.click()
    except exceptions.TimeoutException:
        print('Some thing going wrong')



