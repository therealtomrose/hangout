"""A Script for maintaining persistant google hangouts
"""

import time
import selenium
import urllib2

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
        self.screen_width = settings.SCREEN_WIDTH
        self._getNewDriver()
        self.wait = WebDriverWait(self.driver, 20)

    def xpath_element_is_visible(self, xpath=None, wait_time=10):
        """A custom handler for finding visible elements using xpath that
        doesn't fail while the dom is still loading"""
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
        """A custom handler for finding existing elements using xpath that
        doesn't fail while the dom is still loading"""
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
        """A custom handler for finding elements using css that
        doesn't fail while the dom is still loading"""
        start_time = datetime.now()
        while datetime.now() < start_time + timedelta(seconds=wait_time):
            try:
                element = self.driver.find_element_by_css_selector(element)
                if element.is_displayed():
                    return element
            except:  # Probably can't find the element
                pass
        return None

    def _setUp(self):
        """Start a google hangout session. This is a cascade of events."""
        self.driver.get(self.url)

        element = self.css_element('a.btn-large')
        if element:
            self.driver.get(element.get_attribute("href"))
        element = self.css_element('input#Email')
        if element:
            element.send_keys(self.user_email)
        element = self.css_element('input#Passwd')
        if element:
            element.send_keys(self.user_pass)
        element = self.css_element('input#signIn')
        if element:
            element.click()
        element = self.css_element('input[value="Skip for now"]')
        if element:
            element.click()

        self._handle_join(wait_time=10)

        # Deprecated???
        # try:
        #     self.driver.switch_to_window(self.driver.window_handles[1])
        # except IndexError:
        #     pass  # google hangout opened in the same tab

        self._handle_add_people_to_this_video_call(wait_time=15)
        self._handle_unbounce_continue()
        self._handle_unbounce_hide(wait_time=10)
        print 'New hangout established: ', datetime.now()

    def _tearDown(self):
        """Destroy the current browser session"""
        try:
            self.driver.quit()
        except urllib2.URLError:
            # Not sure what use-case triggers this error. It happens overnight.
            print 'urllib2.URLError: ', datetime.now()

    def _getNewDriver(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(self.screen_width, 600)
        self.driver.maximize_window()

    def _reset(self):
        self._tearDown()
        self._getNewDriver()
        self._setUp()

    def _handle_join(self, wait_time=2):
        element = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "Join")]')
        if element:
            # For some reason, selenium things the join button is visible,
            # when it is really not yet, so we have a work around here
            try:
                element.click()
            except selenium.common.exceptions.WebDriverException:
                # Join not clickable yet
                time.sleep(1)
                self._handle_join(wait_time=wait_time)

    def _handle_add_people_to_this_video_call(self, wait_time=2):
        add_people_tag = self.xpath_element_is_visible(
            xpath='//h1[contains(text(), "Add people")]',
            wait_time=wait_time)
        submit_tag = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "Submit")]',
            wait_time=3)
        if (add_people_tag and submit_tag):
            submit_tag.click()

    def _handle_unbounce_hide(self, wait_time=2):
        try:
            iframe = self.driver.find_elements_by_tag_name('iframe')[1]
            self.driver.switch_to_frame(iframe)
        except IndexError:
            pass  # There is no iframe on this page
        element = self.css_element('div.hide')
        if element:
            element.click()
        hangout.driver.switch_to_default_content()

    def _handle_unbounce_continue(self, wait_time=2):
        tag = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "Continue")]',
            wait_time=wait_time)
        if tag:
            print '"Unhangout Supervisor needs your permission in order to start.": ', datetime.now()
            tag.click()

    def _handle_are_you_still_there(self):
        tag = self.xpath_element_is_visible(
            xpath='//span[contains(text(), "Yes")]',
            wait_time=2)
        if tag:
            print '"Are you still there?": ', datetime.now()
            tag.click()

    def _handle_you_left_the_hangout(self):
        tag = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "You left")]',
            wait_time=2)
        if tag:
            print '"You left the hangout": ', datetime.now()
            self._reset()

    def _handle_found_error(self):
        tag = self.xpath_element_is_visible(
            xpath='//div[contains(text(), "Error")]',
            wait_time=2)
        if tag:
            print 'Error detected: ', datetime.now()
            time.sleep(30)
            self._reset()

    def _handle_hangout_missing(self):
        tag = self.xpath_element_exists(
            xpath='//div[contains(text(), "Chat")]',
            wait_time=5)
        if tag:
            # print 'Hangout is alive: ', datetime.now()
            return False
        else:
            print 'Hangout missing: ', datetime.now()
            self._reset()

    def _browser_is_open(self):
        if self.driver.get_window_position():
            return True
        else:
            # This case causes an un-handle-able error from selenium
            return False

    def run(self):
        self._setUp()
        while True:
            self._handle_are_you_still_there()
            self._handle_unbounce_continue()
            self._handle_you_left_the_hangout()
            self._handle_found_error()
            self._handle_hangout_missing()


if __name__ == '__main__':
    while True:
        hangout = Hangout()
        hangout.run()
