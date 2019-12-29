import webbrowser
from selenium import webdriver
import threading
import time

print('Enter the url of the video you would like to play on repeat: ')
url = input()
# ctr = webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s')
#ctr.open_new_tab(url)

#For removing the "Chrome is being controlled by automated test software" notification
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

# driver = webdriver.Chrome(executable_path='C:/Users/thear/PythonProjects/chromedriver.exe',options=chrome_options)  
driver = webdriver.Chrome(executable_path='C:/Users/thear/PythonProjects/chromedriver.exe')

driver.get('https://www.youtube.com/watch?v=hqbS7O9qIXE&list=RD1jO2wSpAoxA&index=7')

time.sleep(2)
try:
    mainPlayButtonOverlay = driver.find_element_by_class_name('ytp-cued-thumbnail-overlay')
    adSkipSlot = driver.find_element_by_class_name('ytp-ad-player-overlay')
except Exception as e:
    print(e)


if (mainPlayButtonOverlay.is_displayed()):
    print('IN-1')
    mainPlayButton = driver.find_element_by_css_selector('#movie_player > div.ytp-cued-thumbnail-overlay > button')
    mainPlayButton.click()

if (adSkipSlot.is_displayed()):
    print('IN-2')
    while True:
        time.sleep(2)
        try:
            skipButtonSlot = driver.find_elements_by_class_name('ytp-ad-skip-button-slot')
            # skipButtonSlot = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[4]/div/div[3]/div/div[2]')
            if (skipButtonSlot.is_displayed()) :
                skipAd = driver.find_element_by_class_name('ytp-ad-skip-button ytp-button')
                skipAd.click()
                break
        except Exception as e:
            print(e)

print('break')
# def skipAdFunction():
#     print('reached')
#     threading.Timer(3,skipAdFunction).start()
#     if(skipAd.is_enabled() or skipAd.is_displayed()):
#         print('enabled')
#         skipAd.click()

# skipAdFunction()