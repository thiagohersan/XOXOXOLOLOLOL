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
profileLink = mDriver.find_element_by_xpath("//a[@data-testid='blue_bar_profile_link']")
profileHref = profileLink.get_attribute('href')
ActionChains(mDriver).click(profileLink).perform()
sleep(1)

# get link to friends
friendLink = mDriver.find_element_by_xpath("//a[@data-tab-key='friends']")
friendHref = friendLink.get_attribute('href')
mDriver.execute_script("window.scrollTo(%s, %s);"%(friendLink.location['x'], friendLink.location['y']-50))


for i in range(3):
    ActionChains(mDriver).key_down(Keys.SHIFT).click(friendLink).key_up(Keys.SHIFT).perform()

    # huge hack to resize on creation. wtf. seriously?!?
    mDriver.switch_to_window(mDriver.window_handles[-1])
    mDriver.set_window_size(SCREEN_WIDTH/3, SCREEN_HEIGHT)
    mDriver.set_window_position(i*SCREEN_WIDTH/3, 0)
    mDriver.switch_to_window(mDriver.window_handles[0])
    sleep(0.5)
sleep(1)

# close original window
mDriver.switch_to_window(mDriver.window_handles[0])
mDriver.close()


def loadChoseAndScrollFriends():
    # scroll to bottom to load more friends
    for i in range(32):
        for w in mDriver.window_handles:
            if (uniform(0.0,1.0) > 0.5):
                mDriver.switch_to_window(w)
                bodyWidth = mDriver.execute_script("return document.body.scrollWidth;")
                mDriver.execute_script("window.scrollTo(%s, document.body.scrollHeight);"%randint(bodyWidth/5,bodyWidth/2))
                sleep(0.1)

    # chose friends and go to profiles
    for w in mDriver.window_handles:
        mDriver.switch_to_window(w)
        friendList = mDriver.find_elements_by_xpath("//div[@class='fsl fwb fcb']")
        bffLink = friendList[randint(0,len(friendList)-1)]
        mDriver.execute_script("window.scrollTo(%s, %s);"%(bffLink.location['x'], bffLink.location['y']-100))
        bffLink.click()
        sleep(0.5)

    # scroll around a couple of times
    for i in range(32):
        for w in mDriver.window_handles:
            if (uniform(0.0, 1.0) > 0.3):
                mDriver.switch_to_window(w)
                bodyWidth = mDriver.execute_script("return document.body.scrollWidth;")
                bodyHeight = mDriver.execute_script("return document.body.scrollHeight;")
                mDriver.execute_script("window.scrollTo(%s, %s);"%(randint(bodyWidth/8,bodyWidth/2), randint(0,bodyHeight)))

                # like something everyonce in a while
                if(uniform(0.0, 1.0) > 0.7):
                    likeLinks = mDriver.find_elements_by_xpath("//a[@data-testid='fb-ufi-likelink']")
                    if(len(likeLinks) > 1):
                        superLike = likeLinks[randint(0,len(likeLinks)-1)]
                        ActionChains(mDriver).move_to_element(superLike).perform()
                        # TODO: click
                        sleep(0.5)

                # post a comment everyonce in a while
                if(uniform(0.0, 1.0) > 1.9):
                    # TODO: get comment boxes, enter text, send
                    sleep(0.5)
                sleep(0.1)

def backToFriends():
    # go back to list of friends and repeat
    for w in mDriver.window_handles:
        mDriver.switch_to_window(w)
        mDriver.get(friendHref)
        sleep(0.1)
        bodyWidth = mDriver.execute_script("return document.body.scrollWidth;")
        bodyHeight = mDriver.execute_script("return document.body.scrollHeight;")
        mDriver.execute_script("window.scrollTo(%s, %s);"%(randint(bodyWidth/8,bodyWidth/2), randint(0,bodyHeight)))
        sleep(0.1)

def splitWindows():
    # TODO: change this for all windows
    mDriver.switch_to_window(mDriver.window_handles[0])

    # get width/height and position
    #windowWidth = mDriver.execute_script("return window.innerWidth;")
    #windowHeight = mDriver.execute_script("return window.innerHeight;")
    windowX = mDriver.execute_script("return window.screenX;")
    #windowY = mDriver.execute_script("return window.screenY;")

    # find friend list link
    friendLink = mDriver.find_element_by_xpath("//a[@data-tab-key='friends']")
    mDriver.execute_script("window.scrollTo(%s, %s);"%(friendLink.location['x'], friendLink.location['y']-50))

    for i in range(2):
        ActionChains(mDriver).key_down(Keys.SHIFT).click(friendLink).key_up(Keys.SHIFT).perform()

        # huge hack to resize on creation. wtf. seriously?!?
        mDriver.switch_to_window(mDriver.window_handles[-1])
        mDriver.set_window_size(SCREEN_WIDTH/3, SCREEN_HEIGHT/2-10)
        mDriver.set_window_position(windowX, i*(SCREEN_HEIGHT/2)+5)
        mDriver.switch_to_window(mDriver.window_handles[0])
        sleep(0.5)

    # close original window
    mDriver.switch_to_window(mDriver.window_handles[0])
    mDriver.close()

'''
for i in range(8):
    loadChoseAndScrollFriends()
    backToFriends()
'''
