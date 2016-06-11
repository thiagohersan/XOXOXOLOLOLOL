#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from random import uniform, randint
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#####
# http://selenium-python.readthedocs.io/
# http://seleniumhq.github.io/selenium/docs/api/py/api.html
#####

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

# start driver
mOptions = Options()
mOptions.add_argument("user-data-dir=./chromeSettings/")
#mOptions.add_argument("window-size=%s,%s"%(SCREEN_WIDTH,SCREEN_HEIGHT))
#mOptions.add_argument("window-position=0,0")
mDriver = webdriver.Chrome(chrome_options=mOptions)
mDriver.set_window_size(SCREEN_WIDTH, SCREEN_HEIGHT)
mDriver.get('http://www.facebook.com')
mDriver.set_window_position(0,0)
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
sleep(1)

#mDriver.set_window_size(640,400)
#mDriver.set_window_position(0,0)

# get link to profile
mAction = ActionChains(mDriver)
pl = mDriver.find_element_by_xpath("//a[@data-testid='blue_bar_profile_link']")
mAction.click(pl).perform()
sleep(1)

# get link to friends
fl = mDriver.find_element_by_xpath("//a[@data-tab-key='friends']")
fhref = fl.get_attribute('href')
mDriver.execute_script("window.scrollTo(arguments[0], arguments[1]);", fl.location['x'], fl.location['y']-50)
#mAction = ActionChains(mDriver).key_down(Keys.SHIFT).click(fl).key_up(Keys.SHIFT)

for i in range(3):
    ActionChains(mDriver).key_down(Keys.SHIFT).click(fl).key_up(Keys.SHIFT).perform()

    # huge hack to resize on creation. wtf. seriously?!?
    mDriver.switch_to_window(mDriver.window_handles[-1])
    mDriver.set_window_size(SCREEN_WIDTH/3, SCREEN_HEIGHT)
    mDriver.set_window_position(i*SCREEN_WIDTH/3, 0)
    mDriver.switch_to_window(mDriver.window_handles[0])
    sleep(0.5)
sleep(1)

mDriver.switch_to_window(mDriver.window_handles[0])
mDriver.close()


def loadChoseAndScrollFriends():
    # scroll to bottom to load more friends
    for i in range(32):
        for w in mDriver.window_handles:
            if (uniform(0.0,1.0) > 0.5):
                mDriver.switch_to_window(w)
                mw = mDriver.execute_script("return document.body.scrollWidth;")
                mDriver.execute_script("window.scrollTo(%s, document.body.scrollHeight);"%randint(mw/5,mw/2))
                sleep(0.1)

    # chose friends and go to profiles
    for w in mDriver.window_handles:
        mDriver.switch_to_window(w)
        #mDriver.execute_script("window.scrollTo(0, 0);")
        sleep(0.5)
        fls = mDriver.find_elements_by_xpath("//div[@class='fsl fwb fcb']")
        fl = fls[randint(0,len(fls)-1)]
        mDriver.execute_script("window.scrollTo(%s, %s);"%(fl.location['x'], fl.location['y']-100))
        fl.click()
        sleep(0.5)

    # scroll around a couple of times
    for i in range(32):
        for w in mDriver.window_handles:
            if (uniform(0.0, 1.0) > 0.3):
                mDriver.switch_to_window(w)
                mw = mDriver.execute_script("return document.body.scrollWidth;")
                mh = mDriver.execute_script("return document.body.scrollHeight;")
                mDriver.execute_script("window.scrollTo(%s, %s);"%(randint(mw/8,mw/2), randint(0,mh)))
                # everyone in a while like something
                if(uniform(0.0, 1.0) > 0.7):
                    lls = mDriver.find_elements_by_xpath("//a[@data-testid='fb-ufi-likelink']")
                    if(len(lls) > 1):
                        ll = lls[randint(0,len(lls)-1)]
                        ActionChains(mDriver).move_to_element(ll).perform()
                        sleep(0.5)
                sleep(0.1)

def backToFriends():
    # go back to list of friends and repeat
    for w in mDriver.window_handles:
        mDriver.switch_to_window(w)
        mDriver.get(fhref)
        sleep(0.1)
        mw = mDriver.execute_script("return document.body.scrollWidth;")
        mh = mDriver.execute_script("return document.body.scrollHeight;")
        mDriver.execute_script("window.scrollTo(%s, %s);"%(randint(mw/8,mw/2), randint(0,mh)))
        sleep(0.1)



for i in range(8):
    loadChoseAndScrollFriends()
    backToFriends()
loadChoseAndScrollFriends()    
