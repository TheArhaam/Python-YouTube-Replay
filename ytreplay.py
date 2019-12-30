import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import threading
import time

print('Enter the url of the video you would like to play on repeat: ')
url = input() #Taking URL from the user

#Setting up the WebDriver to work with Google Chrome
driver = webdriver.Chrome(executable_path='C:/Users/thear/PythonProjects/chromedriver.exe')

#Loop to refresh and repeat the whole process

#This will launch the url on Google Chrome
#Google Chrome will know that an automated system is accessing it
#Python will wait till the webpage is loaded before moving forward
driver.get(url)

while(True):
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
        adSkipSlot = driver.find_element_by_css_selector('.ytp-ad-player-overlay-skip-or-preview')
        print('Found Ad Player Overlay')

        #If advertisement is being displayed,
        if (adSkipSlot.is_displayed()):
            print('Ad is active')
            while True:
                try:
                    #Getting the Button slot so we can tell if the button is displayed or not
                    skipButtonSlot = driver.find_elements_by_css_selector('.ytp-ad-skip-button-slot')
                    print('Found Skip Button Slot')
                    #Checking if button is displayed
                    if (skipButtonSlot[0].is_displayed()) :
                        print('Skip button is Active')
                        #We click the skip button
                        try:
                            skipAd = driver.find_element_by_css_selector('.ytp-ad-skip-button.ytp-button')
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

    refreshType = 'prev'
    #Get the progress bar
    try:
        progressBar = driver.find_element_by_class_name('ytp-progress-bar ')
        print('Found Progress Bar')
        #Getting Play button
        try:
            playButton = driver.find_element_by_css_selector('.ytp-play-button.ytp-button.ytp-play-button-playlist')
            print('Found Playlist Play Button')
        except Exception as e:
            #If play button is not a playlist play button
            print(e)
            try:
                playButton = driver.find_element_by_css_selector('.ytp-play-button.ytp-button')
                print('Found Play Button')
                refreshType = 'reload'
            except Exception as e:
                print(e)
        prevButton = driver.find_element_by_css_selector('.ytp-prev-button.ytp-button')
        print('Found Prev Button')
        settingsButton = driver.find_element_by_css_selector('.ytp-button.ytp-settings-button.ytp-hd-quality-badge')
        print('Found Settings Button')
        maxVal = int(progressBar.get_attribute('aria-valuemax'))
        while(True):
            try:
                #Opening the settings to make sure progress bar is displayed
                #Values get updated only as long as progress bar is displayed
                settingsButton.click()
            except Exception as e:
                print(e)
            currVal = int(progressBar.get_attribute('aria-valuenow'))
            if(currVal == maxVal-1):
                try:
                    if(refreshType == 'prev'):
                        prevButton.click()
                        print('====================Restarted====================')
                    elif(refreshType == 'reload'):
                        driver.refresh()
                        print('====================Restarted====================')
                        break
                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)