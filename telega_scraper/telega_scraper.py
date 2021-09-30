import re
import time

import requests
import undetected_chromedriver.v2 as uc
from bs4 import BeautifulSoup
from googletrans import Translator
from selenium.webdriver.common.by import By
from telethon.tl.functions.channels import GetFullChannelRequest

from telethon_sign_in import TelethonSignIn

END_URL = 'https://telega.io/catalog?filter%5Bchannel_theme_id%5D=42%2C32%2C16%2C20%2C18&filter%5Bentity_lang%5D=1&filter%5Bviews%5D%5Bmin%5D=100&filter%5Bviews%5D%5Bmax%5D=1000&order%5Bsort%5D=apr&order%5Btype%5D=DESC'
API_ID = 1578213
API_HASH = '94b6e5d761205562494f410c4424c71d'
PHONE_NUMBER = '+972557258155'


def get_channels(url):
    client = TelethonSignIn(API_ID, API_HASH).sign_in_user(PHONE_NUMBER)
    driver = uc.Chrome()
    driver.get(url)

    el = driver.find_element(By.XPATH, '/html/body/div[18]/div[2]/div[4]/div[2]/div/div[2]/div[2]/div[1]')
    while True:
        ints = [int(x) for x in re.findall('\d+', el.text)]
        if ints[0] == ints[1]:
            break

        driver.find_element(By.XPATH,
                            '/html/body/div[18]/div[2]/div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]').click()
        time.sleep(2)

    links_objects = driver.find_element(By.CLASS_NAME, 'right_bar').find_elements(By.TAG_NAME, 'a')
    links = set(
        link.get_property('href') for link in links_objects if 'https://telega.io/' in link.get_property('href'))
    for index, link in enumerate(links):
        r = requests.get(link)
        if r.ok:
            soup = BeautifulSoup(r.text, "html.parser")
            channel_link = soup.find(class_='channel_avatar_link').text
            try:
                channel = client(GetFullChannelRequest(channel_link))
                if not Translator().detect(channel.full_chat.about).lang == 'en':
                    time.sleep(1)
                    continue
                print(f'{index}. {channel_link}')
                time.sleep(1)
            except ValueError:
                time.sleep(1)
                continue
        else:
            time.sleep(1)
            continue


def main():
    print('Script started!')
    get_channels(END_URL)


if __name__ == '__main__':
    main()
