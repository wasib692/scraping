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

username = ""  # twitter username
password = ""  # twitter password


def save_csv_file(data, user):
    print('saving data in csv file...')
    file_name = ''.join(re.findall('\d+', str(datetime.now())))
    path = f'e:/scripts/script1/links/{user}_{file_name}.csv'
    with open(path, 'w', newline='', encoding="utf-8") as csv_file:
        header = ['userName', 'profileLink']
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for i in data:
            writer.writerow(i)


class Twitter(object):
    user_to_scrape = ''  # enter username
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

    # getting profile url
    time.sleep(8)
    driver.get(f'{base_url}{user_to_scrape}')
    time.sleep(10)
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/{}/followers"]'.format(user_to_scrape)))).click()
    time.sleep(20)
    # scrolling
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True
    user_info, links, total_followers = [], [], []
    print('starts scrolling!!!')
    while scrolling:
        for profile in driver.find_elements_by_css_selector('[data-testid="cellInnerDiv"]'):
            try:
                link = profile.find_elements_by_css_selector('a')[0].get_attribute('href')
                if link not in links:
                    users = dict(userName=link.split('/')[-1], profileLink=link)
                    links.append(link)
                    user_info.append(users)
                    total_followers.append(users)
            except Exception as e:
                pass
        if user_info:
            if len(user_info) == 10000:
                try:
                    save_csv_file(user_info, user_to_scrape)
                    user_info = []
                except:
                    print('Issue in saving data to csv.')
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.choice([4, 3, 5]))
        curr_position = driver.execute_script("return window.pageYOffset")

        # check scrolling position
        if last_position == curr_position:
            print('stopped scrolling!!!')
            scrolling = False
        else:
            last_position = curr_position
    driver.close()
    driver.quit()
    save_csv_file(total_followers, user_to_scrape)


if __name__ == '__main__':
    print('starting')
    twitter = Twitter()
    print('finished')
