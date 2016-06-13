#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from random import uniform, randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class State:
    (Home, Profile, FriendList) = range(3)

class ChromeWindow:
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None

    cDriver = None
    profileHref = None
    friendHref = None

    @staticmethod
    def __init__driver__():
        mOptions = Options()
        mOptions.add_argument("user-data-dir=./chromeSettings/")
        #mOptions.add_argument("window-size=%s,%s"%(SCREEN_WIDTH,SCREEN_HEIGHT))
        #mOptions.add_argument("window-position=0,0")
        ChromeWindow.cDriver = webdriver.Chrome(chrome_options=mOptions)
        ChromeWindow.SCREEN_WIDTH = ChromeWindow.cDriver.execute_script("return screen.width;")
        ChromeWindow.SCREEN_HEIGHT = ChromeWindow.cDriver.execute_script("return screen.height;")-24
        ChromeWindow.cDriver.set_window_size(ChromeWindow.SCREEN_WIDTH, ChromeWindow.SCREEN_HEIGHT)
        ChromeWindow.cDriver.set_window_position(0,0)

    @staticmethod
    def __get__profile__element__():
        profileElement = ChromeWindow.cDriver.find_element_by_xpath("//a[@data-testid='blue_bar_profile_link']")
        ChromeWindow.profileHref = profileElement.get_attribute('href')
        return profileElement

    @staticmethod
    def __get__friends__element__():
        friendElement = ChromeWindow.cDriver.find_element_by_xpath("//a[@data-tab-key='friends']")
        ChromeWindow.friendHref = friendElement.get_attribute('href')
        return friendElement

    @staticmethod
    def loginToFacebook():
        ChromeWindow.cDriver.get('http://www.facebook.com')
        # get sign in boxes
        try:
            emailBox = ChromeWindow.cDriver.find_element_by_name('email')
            passwordBox = ChromeWindow.cDriver.find_element_by_name('pass')
        except NoSuchElementException:
            ChromeWindow.cDriver.find_element_by_xpath("//a[@aria-labelledby='userNavigationLabel']").click()
            sleep(2)
            ChromeWindow.cDriver.find_element_by_xpath("//form[@action='https://www.facebook.com/logout.php']").submit()
            sleep(2)
        finally:
            emailBox = ChromeWindow.cDriver.find_element_by_name('email')
            passwordBox = ChromeWindow.cDriver.find_element_by_name('pass')

        # read login/password from file
        secrets = {}
        with open('oauth.txt', 'r') as inFile:
            for line in inFile:
                (k,v) = line.split()
                secrets[k] = v

            # type login/password
            for c in secrets['EMAIL']:
                emailBox.send_keys(c)
                sleep(uniform(0.1, 0.3))
            sleep(0.5)
            for c in secrets['PASSWORD']:
                passwordBox.send_keys(c)
                sleep(uniform(0.1, 0.3))

            passwordBox.submit()


    @staticmethod
    def scroll():
        # for every window object
        #   step()
        pass

    @staticmethod
    def quit():
        ChromeWindow.cDriver.quit()

    def step(self):
        ChromeWindow.cDriver.switch_to_window(self.window_handle)
        if(self.state == State.Home):
            print "state home, going to friend list"
            self.goToFriendList()
        elif(self.state == State.Profile):
            print "state profile"
            if(uniform(0.0,1.0) > 0.95):
                print "   going to friend list or spawn"
                if(uniform(0.0,1.0) > 0.8):
                    print "      going to spawn"
                    self.spawn()
                    # TODO: clean up parent window
                    # TODO: delete object
                    # ChromeWindow.cDriver.switch_to_window(self.window_handle)
                    # ChromeWindow.cDriver.close()
                else:
                    print "      going to friend list"
                    self.goToFriendList()
            elif(uniform(0.0,1.0) > 0.9):
                print "   comment"
                self.postComment()
            elif(uniform(0.0,1.0) > 0.8):
                print "   like"
                self.likePost()
                sleep(0.4)
            else:
                print "   scroll"
                self.scrollProfile()
        elif(self.state == State.FriendList):
            print "friendlist"
            if (uniform(0.0,1.0) > 0.05):
                print "   load scroll"
                self.loadFriends()
            else:
                print "   going to friend"
                self.goToFriend()

    def loadFriends(self):
        if (uniform(0.0,1.0) > 0.5):
            bodyWidth = ChromeWindow.cDriver.execute_script("return document.body.scrollWidth;")
            bodyHeight = ChromeWindow.cDriver.execute_script("return document.body.scrollHeight;")
            ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(randint(bodyWidth/5,bodyWidth/2), bodyHeight))

    def goToFriend(self):
        friendList = ChromeWindow.cDriver.find_elements_by_xpath("//div[@class='fsl fwb fcb']")
        bffLink = friendList[randint(0,len(friendList)-1)]
        ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(bffLink.location['x'], bffLink.location['y']-100))
        bffLink.click()
        self.state = State.Profile

    def scrollProfile(self):
        if (uniform(0.0,1.0) > 0.3):
            bodyWidth = ChromeWindow.cDriver.execute_script("return document.body.scrollWidth;")
            bodyHeight = ChromeWindow.cDriver.execute_script("return document.body.scrollHeight;")
            ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(randint(bodyWidth/8, bodyWidth/2),
                                                                            randint(0, bodyHeight)))

    def likePost(self):
        likeLinks = ChromeWindow.cDriver.find_elements_by_xpath("//a[@data-testid='fb-ufi-likelink']")
        if(len(likeLinks) > 1):
            superLike = likeLinks[randint(0,len(likeLinks)-1)]
            ActionChains(ChromeWindow.cDriver).move_to_element(superLike).perform()
            # TODO: click

    def postComment(self):
        # TODO: get comment boxes/box, enter text, send
        pass

    def spawn(self):
        # TODO: spawn
        #   make sure spawns get correct state (FriendList)
        self.goToFriendList()

    def goToProfile(self):
        ChromeWindow.cDriver.switch_to_window(self.window_handle)
        try:
            profileLink = ChromeWindow.__get__profile__element__()
        except NoSuchElementException:
            ChromeWindow.cDriver.get('http://www.facebook.com')
        finally:
            profileLink = ChromeWindow.__get__profile__element__()
        ActionChains(ChromeWindow.cDriver).click(profileLink).perform()
        self.state = State.Profile

    def goToFriendList(self):
        ChromeWindow.cDriver.switch_to_window(self.window_handle)
        self.goToProfile()
        friendLink = ChromeWindow.__get__friends__element__()
        ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(friendLink.location['x'], friendLink.location['y']-50))
        ActionChains(ChromeWindow.cDriver).click(friendLink).perform()
        self.state = State.FriendList

    def __init__(self, x,y, w,h):
        if(ChromeWindow.cDriver is None):
            ChromeWindow.__init__driver__()

        # x,y,w,h in grid values
        (self.x, self.y, self.w, self.h) = (x,y,w,h)
        self.state = State.Home
        self.window_handle = ChromeWindow.cDriver.window_handles[-1]

