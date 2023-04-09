import os
import random
import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta, date
from selenium.webdriver.support import expected_conditions as ec

username = "" # twitter username
password = "" # twitter password


def save_csv_file(data):
    print('saving data in csv file...')
    file_name = ''.join(re.findall('\d+', str(datetime.now())))
    path = f'e:/scripts/script1/followers_data/file_{file_name}.csv'
    with open(path, 'w', newline='', encoding="utf-8") as csv_file:
        header = ['name', 'link', 'canDm']
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for i in data:
            writer.writerow(i)


# read files
users = []
for i in os.listdir('e:/scripts/script1/links'):
    if i.endswith('.csv'):
        path = 'e:/scripts/script1/links' + '/' + i
        with open(path, 'r', encoding='UTF-8') as f:
            dict_reader = csv.DictReader(f)
            list_of_dict = list(dict_reader)
            for dic in list_of_dict:
                users.append(list(dic.values()))


# get user url and verify user have dm open or not
class GetLinkAndVerifyDm(object):
    base_url = 'https://twitter.com/'
    login_url = "https://twitter.com/i/flow/login"
    driver = webdriver.Edge(executable_path="C:\\Users\\hp\\Downloads\\edgedriver\\msedgedriver.exe")
    wait = WebDriverWait(driver, 25)
    print('driver created!!!')
    # login user
    driver.get(login_url)
    time.sleep(10)
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="username"]'))).send_keys(username)
    if driver.find_elements_by_css_selector('div[role="button"] span span')[1].text == "Next":
        driver.find_elements_by_css_selector('div[role="button"] span span')[1].click()
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="current-password"]'))).send_keys(
        password)
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]'))).click()
    print('logged in!!!')
    time.sleep(10)
    value = True
    user_lists = []
    while value:
        if users:
            for i in users:
                time.sleep(1)
                driver.get(f'{base_url}{i[0]}')
                time.sleep(3)
                try:
                    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]  a')))
                    dm_status = False
                    if driver.find_element_by_css_selector('[aria-label="Message"]'):
                        dm_status = True
                except:
                    dm_status = False
                user = dict(name=i[0],
                            link=i[1],
                            canDm=dm_status)
                user_lists.append(user)
                time.sleep(1)
                if user_lists and len(user_lists) == 10000:
                    save_csv_file(user_lists)
                    user_lists = []
            save_csv_file(user_lists)
            value = False
            driver.close()
            driver.quit()


if __name__ == '__main__':
    print('starting')
    GetLinkAndVerifyDm()
    print('finished')
