#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from random import uniform, randint, choice
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

COMMENTS = ["#FORATEMER",
            "LOL",
            "XOXO",
            "XOXOXOLOLOLOL"]

class State:
    (Home, MyProfile, Profile, FriendList) = range(4)

class ChromeWindow:
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None

    cDriver = None
    profileHref = None
    friendHref = None

    windows = []

    @staticmethod
    def __init__driver__():
        mOptions = Options()
        mOptions.add_argument("user-data-dir=./chromeSettings/")
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
        try:
            emailBox = ChromeWindow.cDriver.find_element_by_name('email')
            passwordBox = ChromeWindow.cDriver.find_element_by_name('pass')
        except NoSuchElementException:
            expectedMenu = EC.presence_of_element_located((By.XPATH, "//a[@aria-labelledby='userNavigationLabel']"))
            navigationMenu = WebDriverWait(ChromeWindow.cDriver, 2, 0.2).until(expectedMenu)
            navigationMenu.click()

            expectedForm = EC.presence_of_element_located((By.XPATH, "//form[@action='https://www.facebook.com/logout.php']"))
            logoutForm = WebDriverWait(ChromeWindow.cDriver, 2, 0.2).until(expectedForm)
            logoutForm.submit()
        finally:
            expectedEmail = EC.presence_of_element_located((By.NAME, "email"))
            emailBox = WebDriverWait(ChromeWindow.cDriver, 2, 0.2).until(expectedEmail)
            expectedPass = EC.presence_of_element_located((By.NAME, "pass"))
            passwordBox = WebDriverWait(ChromeWindow.cDriver, 2, 0.2).until(expectedPass)

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
            passwordBox.send_keys(Keys.ENTER)


    @staticmethod
    def run():
        for w in ChromeWindow.windows:
            w.step()

    @staticmethod
    def quit():
        ChromeWindow.cDriver.quit()

    def step(self):
        ChromeWindow.cDriver.switch_to_window(self.window_handle)
        if(self.state == State.Home):
            print "state home, going to my profile"
            self.goToMyProfile()
        elif(self.state == State.MyProfile):
            print "state myprofile"
            if(uniform(0.0,1.0) > 0.8):
                print "   going to spawn"
                #self.spawn()
                self.goToFriendList()
            else:
                print "   going to friend list"
                self.goToFriendList()
        elif(self.state == State.Profile):
            print "state profile"
            if(uniform(0.0,1.0) > 0.95):
                print "   going back to myprofile"
                self.goToMyProfile()
            elif(uniform(0.0,1.0) > 0.9):
                print "   comment"
                self.postComment()
            elif(uniform(0.0,1.0) > 0.8):
                print "   like"
                self.likePost()
            else:
                print "   scroll"
                self.scrollProfile()
        elif(self.state == State.FriendList):
            print "state friendlist"
            if (uniform(0.0,1.0) > 0.1):
                print "   load/scroll"
                self.loadFriends()
            else:
                print "   going to friend"
                self.goToFriend()

    def loadFriends(self):
        if (uniform(0.0,1.0) > 0.3):
            bodyWidth = ChromeWindow.cDriver.execute_script("return document.body.scrollWidth;")
            bodyHeight = ChromeWindow.cDriver.execute_script("return document.body.scrollHeight;")
            ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(randint(bodyWidth/5,bodyWidth/2), bodyHeight))

    def goToFriend(self):
        friendList = ChromeWindow.cDriver.find_elements_by_xpath("//div[@class='fsl fwb fcb']")
        bffLink = choice(friendList)
        ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(bffLink.location['x'], bffLink.location['y']-100))
        sleep(0.1)
        bffLink.click()
        # TODO: investigate and make sure it always goes to a friend
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
            superLike = choice(likeLinks)
            windowHeightCenter = ChromeWindow.cDriver.execute_script("return window.innerHeight;")/2
            ChromeWindow.cDriver.execute_script("window.scrollTo(0, %s);"%(superLike.location['y']-windowHeightCenter))
            ActionChains(ChromeWindow.cDriver).move_to_element(superLike).perform()
            sleep(0.5)
            #superLike.click()
            #sleep(0.5)

    def postComment(self):
        try:
            commentForms = ChromeWindow.cDriver.find_elements_by_xpath("//div[@class='UFICommentContainer']")
            if(len(commentForms) > 1):
                commentBox = choice(commentForms)
                windowHeightCenter = ChromeWindow.cDriver.execute_script("return window.innerHeight;")/2
                ChromeWindow.cDriver.execute_script("window.scrollTo(0, %s);"%(commentBox.location['y']-windowHeightCenter))
                commentBox.click()
                expectedTextBox = EC.presence_of_element_located((By.XPATH, "//div[@data-testid='ufi_comment_composer']"))
                commentBoxText = WebDriverWait(ChromeWindow.cDriver, 1, 0.1).until(expectedTextBox)
                sleep(0.1)
                for c in choice(COMMENTS):
                    commentBoxText.send_keys(c)
                    sleep(uniform(0.1, 0.3))
                sleep(0.5)
                #commentBoxText.send_keys(Keys.ENTER)
                offsetX = ChromeWindow.cDriver.execute_script("return window.pageXOffset;")
                offsetY = ChromeWindow.cDriver.execute_script("return window.pageYOffset;")
                windowHeight = ChromeWindow.cDriver.execute_script("return window.innerHeight;")
                ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(offsetX, offsetY+windowHeight))
                for i in range(16):
                    commentBoxText.send_keys(Keys.BACKSPACE)
        except Exception as e:
            print "comment exception (???)"

    def spawn(self, spawnElementXPath="//a[@data-tab-key='friends']"):
        # IMPORTANT:
        #     assumes current window is the window to be spawned and closed
        #     assumes we're in State.myProfile
        SCREEN_WIDTH = ChromeWindow.SCREEN_WIDTH
        SCREEN_HEIGHT = ChromeWindow.SCREEN_HEIGHT
        spawnElement = ChromeWindow.cDriver.find_element_by_xpath(spawnElementXPath)

        # break vertically
        if (self.w >= self.h) and (self.w > 1):
            w0 = choice(range(1, self.w))
            w1 = self.w - w0

            ActionChains(ChromeWindow.cDriver).key_down(Keys.SHIFT).click(spawnElement).key_up(Keys.SHIFT).perform()
            window0 = ChromeWindow(self.x, self.y, w0, self.h)
            ChromeWindow.cDriver.switch_to_window(ChromeWindow.cDriver.window_handles[-1])
            ChromeWindow.cDriver.set_window_size(w0*SCREEN_WIDTH/3, self.h*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.set_window_position(self.x*SCREEN_WIDTH/3, self.y*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.switch_to_window(self.window_handle)
            sleep(0.5)

            ActionChains(ChromeWindow.cDriver).key_down(Keys.SHIFT).click(spawnElement).key_up(Keys.SHIFT).perform()
            window1 = ChromeWindow(self.x+w0, self.y, w1, self.h)
            ChromeWindow.cDriver.switch_to_window(ChromeWindow.cDriver.window_handles[-1])
            ChromeWindow.cDriver.set_window_size(w1*SCREEN_WIDTH/3, self.h*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.set_window_position((self.x+w0)*SCREEN_WIDTH/3, self.y*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.switch_to_window(self.window_handle)
            sleep(0.5)

            window0.state = State.FriendList
            window1.state = State.FriendList
            ChromeWindow.cDriver.switch_to_window(self.window_handle)
            ChromeWindow.cDriver.close()
            ChromeWindow.windows.remove(self)

        # break horizontally
        elif (self.h > 1):
            h0 = choice(range(1, self.h))
            h1 = self.h - h0

            ActionChains(ChromeWindow.cDriver).key_down(Keys.SHIFT).click(spawnElement).key_up(Keys.SHIFT).perform()
            window0 = ChromeWindow(self.x, self.y, self.w, h0)
            ChromeWindow.cDriver.switch_to_window(ChromeWindow.cDriver.window_handles[-1])
            ChromeWindow.cDriver.set_window_size(self.w*SCREEN_WIDTH/3, h0*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.set_window_position(self.x*SCREEN_WIDTH/3, self.y*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.switch_to_window(self.window_handle)
            sleep(0.5)

            ActionChains(ChromeWindow.cDriver).key_down(Keys.SHIFT).click(spawnElement).key_up(Keys.SHIFT).perform()
            window1 = ChromeWindow(self.x, self.y+h0, self.w, h1)
            ChromeWindow.cDriver.switch_to_window(ChromeWindow.cDriver.window_handles[-1])
            ChromeWindow.cDriver.set_window_size(self.w*SCREEN_WIDTH/3, h1*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.set_window_position(self.x*SCREEN_WIDTH/3, (self.y+h0)*SCREEN_HEIGHT/3-10)
            ChromeWindow.cDriver.switch_to_window(self.window_handle)
            sleep(0.5)

            window0.state = State.FriendList
            window1.state = State.FriendList
            ChromeWindow.cDriver.switch_to_window(self.window_handle)
            ChromeWindow.cDriver.close()
            ChromeWindow.windows.remove(self)

    def goToMyProfile(self):
        ChromeWindow.cDriver.switch_to_window(self.window_handle)
        try:
            profileLink = ChromeWindow.__get__profile__element__()
        except NoSuchElementException:
            ChromeWindow.cDriver.get('http://www.facebook.com')
        finally:
            profileLink = ChromeWindow.__get__profile__element__()
        ChromeWindow.cDriver.get(ChromeWindow.profileHref)
        self.state = State.MyProfile

    def goToFriendList(self):
        ChromeWindow.cDriver.switch_to_window(self.window_handle)
        try:
            friendLink = ChromeWindow.__get__friends__element__()
        except NoSuchElementException:
            self.state = State.Home
            return
        finally:
            friendLink = ChromeWindow.__get__friends__element__()

        ChromeWindow.cDriver.execute_script("window.scrollTo(%s, %s);"%(friendLink.location['x'], friendLink.location['y']-50))
        ActionChains(ChromeWindow.cDriver).click(friendLink).perform()
        self.state = State.FriendList

    def __init__(self, x=0,y=0, w=3,h=3):
        if(ChromeWindow.cDriver is None):
            ChromeWindow.__init__driver__()

        # x,y,w,h in grid values
        (self.x, self.y, self.w, self.h) = (x,y,w,h)
        self.state = State.Home
        self.window_handle = ChromeWindow.cDriver.window_handles[-1]
        ChromeWindow.windows.append(self)

if __name__ == "__main__":
    mW = ChromeWindow()
    ChromeWindow.loginToFacebook()
    for i in range(64):
        print i
        ChromeWindow.run()
        sleep(0.5)
