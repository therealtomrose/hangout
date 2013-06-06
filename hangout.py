"""A Script for maintaining persistant google hangouts
"""

from datetime import datetime
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import settings_local as settings

class Hangout():
    def __init__(self):
        self.url = settings.HANGOUT_URL
        self.user_email = settings.HANGOUT_USER_EMAIL
        self.user_pass = settings.HANGOUT_USER_PASS
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1024, 600)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def xpath_element(self, xpath=None, wait_time=10):
        start_time = datetime.now()
        while datetime.now() < start_time + timedelta(seconds=wait_time):
            element = None
            try:
                element = self.driver.find_element(by=By.XPATH, value=xpath)
                if element.is_displayed():
                    return element
            except:
                pass
        return None

    def css_element(self, element=None, wait_time=10):
        start_time = datetime.now()
        while datetime.now() < start_time + timedelta(seconds=wait_time):
            element = self.driver.find_element_by_css_selector(element)
            if element.is_displayed():
                return element
        return None

    def setUp(self):
        self.driver.get(self.url)
        self.css_element('input#Email').send_keys(self.user_email)
        self.css_element('input#Passwd').send_keys(self.user_pass)
        self.css_element('input#signIn').click()
        self.xpath_element(xpath='//div[contains(text(), "Join")]').click()

    def tearDown(self):
        self.driver.quit()

    def maintain_hangout(self):
        while True:
            tag = self.xpath_element(xpath='//div[contains(text(), "You left")]')
            if tag:
                return None

if __name__ == '__main__':
    while True:
        hangout = Hangout()
        hangout.setUp()
        hangout.maintain_hangout()
        hangout.tearDown()
