"""A Script for maintaining persistant google hangouts
"""

import time

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
        print dir(self.driver)
        self.driver.set_window_size(1024, 600)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def xpath_element_is_visible(self, xpath=None, wait_time=10):
        start_time = datetime.now()
        while datetime.now() < start_time + timedelta(seconds=wait_time):
            element = None
            try:
                element = self.driver.find_element(by=By.XPATH, value=xpath)
                if element.is_displayed():
                    return element
            except:  # Probably can't find the element
                pass
        return None

    def xpath_element_exists(self, xpath=None, wait_time=10):
        start_time = datetime.now()
        while datetime.now() < start_time + timedelta(seconds=wait_time):
            element = None
            try:
                element = self.driver.find_element(by=By.XPATH, value=xpath)
                if element:
                    return element
            except:  # Probably can't find the element
                pass
        return None

    def css_element(self, element=None, wait_time=10):
        start_time = datetime.now()
        while datetime.now() < start_time + timedelta(seconds=wait_time):
            try:
                element = self.driver.find_element_by_css_selector(element)
                if element.is_displayed():
                    return element
            except:  # Probably can't find the element
                pass
        return None

    def setUp(self):
        self.driver.get(self.url)
        element = self.css_element('input#Email')
        if element:
            element.send_keys(self.user_email)
        element = self.css_element('input#Passwd')
        if element:
            element.send_keys(self.user_pass)
        element = self.css_element('input#signIn')
        if element:
            element.click()
        element = self.xpath_element_is_visible(xpath='//div[contains(text(), "Join")]')
        if element:
            element.click()

    def tearDown(self):
        return True
        # self.driver.quit()

    def reset(self):
        self.tearDown()
        self.setUp()

    def _handle_are_you_still_there(self):
        tag = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "Yes")]',
            wait_time=2)
        if tag:
            tag.click()

    def _you_left_the_hangout(self):
        tag = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "You left")]',
            wait_time=2)
        if tag:
            return True

    def _found_error(self):
        tag = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "Error")]',
            wait_time=2)
        if tag:
            return True

    def _hangout_missing(self):
        tag = self.xpath_element_exists(
            xpath='//div[contains(text(), "Invite people")]',
            wait_time=5)
        if tag:
            print 'Hangout is alive: ', datetime.now()
            return False
        else:
            return True

    def run(self):
        self.setUp()
        while True:
            self._handle_are_you_still_there()
            if self._you_left_the_hangout():
                self.reset()
            if self._found_error():
                time.sleep(30)
                self.reset()
            if self._hangout_missing():
                self.reset()
            print self.driver.session_id


if __name__ == '__main__':
    while True:
        hangout = Hangout()
        hangout.run()
