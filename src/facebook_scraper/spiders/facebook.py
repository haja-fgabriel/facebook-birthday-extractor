# -*- coding: utf-8 -*-
from datetime import datetime
import os
from itertools import chain
import time

import ipdb
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from facebook_scraper.items import FacebookProfile

FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")
FACEBOOK_EMAIL = os.getenv("FACEBOOK_EMAIL")

path_cookies_moreoptions = (
    '//button[@data-cookiebanner="manage_button" and @data-testid="cookie-policy-dialog-manage-button"]'
)
path_cookies_accept_onlyessential = '//button[@data-cookiebanner="accept_only_essential_button" and @data-testid="cookie-policy-manage-dialog-accept-button"]'
path_input_email = '//input[@id="email"]'
path_input_password = '//input[@id="pass"]'
path_searchbar = '//input[@placeholder="Search Facebook"]'
path_birthdays_searchresult = '//a[@href="https://www.facebook.com/events/birthdays"]'
path_login = '//button[@data-testid="royal_login_button"]'
path_div_birthday_container = '//span[contains(text(), "{text}")]/ancestor::div[@class="sjgh65i0"]'
path_div_todays_birthdays = path_div_birthday_container.format(text="Today's Birthdays")
path_div_recent_birthdays = path_div_birthday_container.format(text="Recent Birthdays")
path_div_upcoming_birthdays = path_div_birthday_container.format(text="Upcoming Birthdays")
path_birthday_entry = './/div[@class="dati1w0a qt6c0cv9 hv4rvrfc jb3vyjys b20td4e0"]/div[@class]'
path_entry_name = './/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn iv3no6db gfeo3gy3 a3bd9o3v lrazzd5p oo9gr5id"]'
path_birthday_entry_birthday = './/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 tia6h79c mdeji52x sq6gx45u a3bd9o3v b1v8xokw m9osqain"]'

opts = webdriver.ChromeOptions()
# opts.add_argument("headless")


class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["facebook.com"]
    start_urls = ["http://books.toscrape.com/"]

    def __click_from_js(self, element):
        self.driver.execute_script("arguments[0].click()", element)

    def login(self):
        self.driver.get("https://facebook.com")
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, path_cookies_moreoptions)))

        button_cookies_moreoptions = self.driver.find_element(By.XPATH, path_cookies_moreoptions)
        button_cookies_moreoptions.click()

        time.sleep(2)
        button_cookies_accept_onlyessential = self.driver.find_element(By.XPATH, path_cookies_accept_onlyessential)
        button_cookies_accept_onlyessential.click()

        time.sleep(1)

        input_email = self.driver.find_element(By.XPATH, path_input_email)
        input_password = self.driver.find_element(By.XPATH, path_input_password)

        input_email.send_keys(FACEBOOK_EMAIL)
        input_password.send_keys(FACEBOOK_PASSWORD)

        button_login = self.driver.find_element(By.XPATH, path_login)
        self.__click_from_js(button_login)

    def get_todays_birthdays(self):
        div_todays_birthdays = self.driver.find_element(By.XPATH, path_div_todays_birthdays)
        for div in div_todays_birthdays.find_elements(By.XPATH, path_birthday_entry):
            profile = FacebookProfile()
            profile["link"] = div.find_element(By.TAG_NAME, "a").get_attribute("href")
            profile["name"] = div.find_element(By.XPATH, path_entry_name).text
            profile["birthday"] = datetime.now().astimezone()
            yield profile

    def get_recent_birthdays(self):
        div_recent_birthdays = self.driver.find_element(By.XPATH, path_div_recent_birthdays)
        for div in div_recent_birthdays.find_elements(By.XPATH, path_birthday_entry):
            profile = FacebookProfile()
            profile["link"] = div.find_element(By.TAG_NAME, "a").get_attribute("href")
            profile["name"] = div.find_element(By.XPATH, path_entry_name).text
            birthday = div.find_element(By.XPATH, path_birthday_entry_birthday).text
            birthday_format = "%B %d, %Y" if len(birthday.split(" ")) >= 3 else "%B %d"
            profile["birthday"] = datetime.strptime(birthday, birthday_format)
            yield profile

    def get_upcoming_birthdays(self):
        div_recent_birthdays = self.driver.find_element(By.XPATH, path_div_upcoming_birthdays)
        for div in div_recent_birthdays.find_elements(By.XPATH, path_birthday_entry):
            profile = FacebookProfile()
            profile["link"] = div.find_element(By.TAG_NAME, "a").get_attribute("href")
            profile["name"] = div.find_element(By.XPATH, path_entry_name).text
            birthday = div.find_element(By.XPATH, path_birthday_entry_birthday).text
            birthday_format = "%B %d, %Y" if len(birthday.split(" ")) >= 3 else "%B %d"
            profile["birthday"] = datetime.strptime(birthday, birthday_format)
            yield profile

    def get_all_birthdays(self):
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, path_searchbar)))
        searchbar = self.driver.find_element(By.XPATH, path_searchbar)
        self.__click_from_js(searchbar)
        searchbar.send_keys("birthdays")

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, path_birthdays_searchresult)))
        birthdays_searchresult = self.driver.find_element(By.XPATH, path_birthdays_searchresult)
        self.__click_from_js(birthdays_searchresult)

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//h1[text()="Events"]')))
        for profile in chain(
            self.get_todays_birthdays(),
            self.get_recent_birthdays(),
            self.get_upcoming_birthdays(),
        ):
            yield profile

    def parse(self, response):
        if not FACEBOOK_EMAIL or not FACEBOOK_PASSWORD:
            raise Exception(
                "Login cannot be done. Please set the FACEBOOK_EMAIL and the FACEBOOK_PASSWORD environment variables."
            )
        self.driver = webdriver.Chrome(
            os.path.join(os.pardir, "chromedriver"),
            chrome_options=opts,
        )

        self.login()
        for person in self.get_all_birthdays():
            yield person

        time.sleep(10)
        self.driver.quit()
