import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import threading
import time

print('Enter the url of the video you would like to play on repeat: ')
url = input() #Taking URL from the user

#Setting up the WebDriver to work with Google Chrome
driver = webdriver.Chrome(executable_path='C:/Users/thear/PythonProjects/chromedriver.exe')

#This will launch the url on Google Chrome
#Google Chrome will know that an automated system is accessing it
#Python will wait till the webpage is loaded before moving forward
driver.get(url)

#Video doesn't seem to autstart
#So we're checking if the play button is displayed
try:
    mainPlayButtonOverlay = driver.find_element_by_class_name('ytp-cued-thumbnail-overlay')
except Exception as e:
    print(e)

#If the play button is displayed we click on it and autostart the video
if (mainPlayButtonOverlay.is_displayed()):
    print('IN-1')
    mainPlayButton = driver.find_element_by_css_selector('#movie_player > div.ytp-cued-thumbnail-overlay > button')
    mainPlayButton.click()

#Checking if Advertisement is being displayed
try:
    adSkipSlot = driver.find_element_by_class_name('ytp-ad-player-overlay')
except Exception as e:
    print(e)

#If advertisement is being displayed,
if (adSkipSlot.is_displayed()):
    print('IN-2')
    while True:
        time.sleep(2)
        try:
            #Getting the Button slot so we can tell if the button is displayed or not
            skipButtonSlot = driver.find_elements_by_css_selector('.ytp-ad-skip-button-slot')
            #Checking if button is displayed
            if (skipButtonSlot.is_displayed()) :
                #We click the skip button
                skipAd = driver.find_element_by_class_name('ytp-ad-skip-button ytp-button')
                skipAd.click()
                break
        except Exception as e:
            print(e)

print('break')