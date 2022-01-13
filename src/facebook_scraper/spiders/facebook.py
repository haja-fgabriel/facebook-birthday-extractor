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
        self.wait_for_element(path_cookies_moreoptions)

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

    def parse_date(self, date):
        format = "%B %d, %Y" if len(date.split(" ")) >= 3 else "%B %d"
        return datetime.strptime(date, format)

    def get_todays_birthdays(self):
        return self.get_profiles(path_div_todays_birthdays, is_today=True)

    def get_recent_birthdays(self):
        return self.get_profiles(path_div_recent_birthdays)

    def get_upcoming_birthdays(self):
        return self.get_profiles(path_div_upcoming_birthdays)

    def get_profiles(self, container_path, is_today=False):
        div_recent_birthdays = self.driver.find_element(By.XPATH, container_path)
        for div in div_recent_birthdays.find_elements(By.XPATH, path_birthday_entry):
            profile = FacebookProfile()
            profile["link"] = div.find_element(By.TAG_NAME, "a").get_attribute("href")
            profile["name"] = div.find_element(By.XPATH, path_entry_name).text
            if is_today:
                profile["birthday"] = datetime.now().astimezone()
            else:
                birthday = div.find_element(By.XPATH, path_birthday_entry_birthday).text
                profile["birthday"] = self.parse_date(birthday)
            yield profile

    def navigate_to_birthdays(self):
        self.wait_for_main_page_searchbar()
        searchbar = self.driver.find_element(By.XPATH, path_searchbar)
        self.__click_from_js(searchbar)
        searchbar.send_keys("birthdays")

        self.wait_for_element(path_birthdays_searchresult)
        birthdays_searchresult = self.driver.find_element(By.XPATH, path_birthdays_searchresult)
        self.__click_from_js(birthdays_searchresult)
        self.wait_for_birthdays_page()

    def wait_for_main_page_searchbar(self):
        self.wait_for_element(path_searchbar)

    def wait_for_birthdays_page(self):
        self.wait_for_element('//h1[text()="Events"]')

    def wait_for_element(self, xpath, timeout=10):
        WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located((By.XPATH, xpath)))

    def get_all_birthdays(self):
        self.navigate_to_birthdays()
        for profile in chain(
            self.get_todays_birthdays(),
            self.get_recent_birthdays(),
            self.get_upcoming_birthdays(),
        ):
            yield profile

    def validate_login(self):
        if not FACEBOOK_EMAIL or not FACEBOOK_PASSWORD:
            raise Exception(
                "Login cannot be done. Please set the FACEBOOK_EMAIL and the FACEBOOK_PASSWORD environment variables."
            )

    def init_driver(self):
        self.driver = webdriver.Chrome(
            os.path.join(os.pardir, "chromedriver"),
            chrome_options=opts,
        )

    def parse(self, response):
        self.validate_login()
        self.init_driver()
        self.login()
        for person in self.get_all_birthdays():
            yield person

        time.sleep(10)
        self.driver.quit()
