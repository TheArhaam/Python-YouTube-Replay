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
    print('Found Main Play Button Overlay')
except Exception as e:
    print(e)

#If the play button is displayed we click on it and autostart the video
if (mainPlayButtonOverlay.is_displayed()):
    print('Video did not start')
    try:
        mainPlayButton = driver.find_element_by_css_selector('#movie_player > div.ytp-cued-thumbnail-overlay > button')
        print('Found Main Play Button')
    except Exception as e:
        print(e)
    mainPlayButton.click()
    print('Started video')

#Checking if Advertisement is being displayed
try:
    adSkipSlot = driver.find_element_by_class_name('ytp-ad-player-overlay-skip-or-preview')
    print('Found Ad Player Overlay')

    #If advertisement is being displayed,
    if (adSkipSlot.is_displayed()):
        print('Ad is active')
        while True:
            time.sleep(2)
            try:
                #Getting the Button slot so we can tell if the button is displayed or not
                skipButtonSlot = driver.find_elements_by_css_selector('.ytp-ad-skip-button-slot')
                print('Found Skip Button Slot')
                #Checking if button is displayed
                if (skipButtonSlot.is_displayed()) :
                    print('Skip button is Active')
                    #We click the skip button
                    try:
                        skipAd = driver.find_element_by_class_name('ytp-ad-skip-button ytp-button')
                        print('Found Skip Button')
                    except Exception as e:
                        print(e)
                    skipAd.click()
                    print('Skipped Ad')
                    break
            except Exception as e:
                print(e)
except Exception as e:
    print(e)

#Get the progress bar
try:
    progressBar = driver.find_element_by_class_name('ytp-progress-bar ')
    print('Found Progress Bar')
    currVal = progressBar.get_attribute('aria-valuenow')
    maxVal = progressBar.get_attribute('aria-valuemax')
    print(currVal,maxVal)
except Exception as e:
    print(e)