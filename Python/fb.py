#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from random import uniform
from selenium import webdriver

# read login/password from file
secrets = {}
with open('oauth.txt', 'r') as inFile:
    for line in inFile:
        (k,v) = line.split()
        secrets[k] = v

# start driver
mDriver = webdriver.Chrome()
mDriver.get('http://www.facebook.com');
sleep(1)
emailBox = mDriver.find_element_by_name('email')
passwordBox = mDriver.find_element_by_name('pass')

# type login/password
for c in secrets['EMAIL']:
    emailBox.send_keys(c)
    sleep(uniform(0.1,0.5))
for c in secrets['PASSWORD']:
    passwordBox.send_keys(c)
    sleep(uniform(0.1,0.5))

passwordBox.submit()
sleep(10)

mDriver.quit()
