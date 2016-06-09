#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from random import uniform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# start driver
mOptions = Options()
mOptions.add_argument("user-data-dir=./chromeSettings/")
mDriver = webdriver.Chrome(chrome_options=mOptions)
mDriver.get('http://www.facebook.com');
sleep(1)
emailBox = mDriver.find_element_by_name('email')
passwordBox = mDriver.find_element_by_name('pass')


# read login/password from file
secrets = {}
with open('oauth.txt', 'r') as inFile:
    for line in inFile:
        (k,v) = line.split()
        secrets[k] = v

# type login/password
for c in secrets['EMAIL']:
    emailBox.send_keys(c)
    sleep(uniform(0.1,0.4))
sleep(0.6)
for c in secrets['PASSWORD']:
    passwordBox.send_keys(c)
    sleep(uniform(0.1,0.4))

passwordBox.submit()
sleep(10)

mDriver.quit()
