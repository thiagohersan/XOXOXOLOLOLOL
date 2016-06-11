#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from random import uniform
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#####
# http://selenium-python.readthedocs.io/
#####

# start driver
mOptions = Options()
mOptions.add_argument("user-data-dir=./chromeSettings/")
mOptions.add_argument("window-size=1280,800")
mOptions.add_argument("window-position=0,0")
mDriver = webdriver.Chrome(chrome_options=mOptions)
mAction = ActionChains(mDriver)
mDriver.get('http://www.facebook.com')
sleep(1)

# get sign in boxes
# TODO: catch exception and logout?
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
    sleep(uniform(0.1,0.3))
sleep(0.5)
for c in secrets['PASSWORD']:
    passwordBox.send_keys(c)
    sleep(uniform(0.1,0.3))

passwordBox.submit()
sleep(2)

current = {}
(current['x'], current['y']) = (0,0)

# get all likes for the initial load
mDriver.execute_script("window.scrollTo(0, 0);")
likes = mDriver.find_elements_by_class_name("UFILikeLink")

# get first like by element and move there
for l in likes:
    if ("fb-ufi-likelink" in l.get_attribute("data-testid")):
        print "%s, %s"%(l.location['x'], l.location['y'])
        (current['x'], current['y']) = (l.location['x'], l.location['y'])
        mAction.move_to_element(l).perform()
        break

# load 5 times and keep moving from like button to like button
for i in range(50):
    print "load %s"%i
    for l in likes:
        if ("fb-ufi-likelink" in l.get_attribute("data-testid")):
            print "%s, %s"%(l.location['x'], l.location['y'])
            (diffX, diffY) = (l.location['x']-current['x'], l.location['y']-current['y'])
            mDriver.execute_script("window.scrollBy(arguments[0], arguments[1]);", diffX, diffY)
            #mAction.move_to_element(l).perform()
            (current['x'], current['y']) = (l.location['x'], l.location['y'])
            sleep(3)
            #CLICK!!!
            #sleep(1)

    likes = [l for l in mDriver.find_elements_by_class_name("UFILikeLink") if l.location['y'] > current['y']]

mDriver.quit()
