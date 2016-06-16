#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from random import uniform, randint
from selenium import webdriver
from ChromeWindow import ChromeWindow

class TestSpawn(ChromeWindow):
    def step(self):
        TestSpawn.cDriver.switch_to_window(self.window_handle)
        if(uniform(0.0,1.0) > 0.33):
            print "scroll"
            self.scroll()
        else:
            print "spawn"
            self.spawn("//a[@href='/']")

    def scroll(self):
        bodyHeight = TestSpawn.cDriver.execute_script("return document.body.scrollHeight;")
        TestSpawn.cDriver.execute_script("window.scrollTo(0, %s);"%(randint(0, bodyHeight)))

    ChromeWindow.step = step
    ChromeWindow.scroll = scroll

if __name__ == "__main__":
    mW = TestSpawn()
    TestSpawn.cDriver.get("http://www.bbc.com/")
    for i in range(64):
        print i
        TestSpawn.run()
        sleep(0.5)
