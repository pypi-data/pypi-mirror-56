#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_element(self, css):
        ''' Try to select an element from the dom via a css selecor
            Returns None if no element was found '''
        self.driver.implicitly_wait(3)

        try:
            return self.driver.find_element_by_css_selector(css)
        except Exception:
            pass

    def get_elements(self, css):
        ''' Try to select every element from the dom via a css selecor
            Returns None if no element was found '''
        try:
            return self.driver.find_elements_by_css_selector(css)
        except Exception:
            pass

    def click_element(self, element):
        ''' Try to click on an element
            Returns None if element was not found or not clickable'''
        if element is None:
            # element not found
            return

        try:
            element.click()
        except Exception:
            # not clickable
            return

    def load_url(self, url, force=False):
        ''' Load an url via the get method '''
        if url != self.driver.current_url or force:
            self.driver.get(url)

    def input_element(self, element, input):
        ''' Fill an input element '''
        if element:
            element.clear()
            element.send_keys(input)

    def get_element_text(self, css):
        ''' Try to select an image and get its content
            Returns None if no element or text was found '''
        element = self.get_element(css)

        if element is None:
            # no element found
            return False

        return element.text

    def send_enter(self, element):
        element.send_keys(Keys.RETURN)

    def wait(self, min=1, max=10):
        ''' Waits a few seconds between 1 and max value'''
        time.sleep(random.randint(min, max))

    def close(self):
        self.driver.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
