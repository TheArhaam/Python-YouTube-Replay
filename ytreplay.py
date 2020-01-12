import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import threading
import time
import re
#For UI
import tkinter
from tkinter import *
import os
from PIL import Image, ImageTk

# ====================== TO DO LIST ====================== 
# Get the name of the video and display it in the UI [DONE]
# Not able to pause video - FIX IT   [DONE (UNTESTED)]
# Figure out how to close the browser when submit button is pressed again
#   -Something to do with threading
#   -Figure out how to stop the thread and close the driver within that thread
# Display "Video Title" only when submit button is pressed and title is set

def clickHandle():
    def mainfunc():
        url = urlEntry.get()
        #Setting up the WebDriver to work with Google Chrome
        driver = webdriver.Chrome(
            executable_path='C:/Users/thear/PythonProjects/chromedriver.exe')
        #This will launch the url on Google Chrome
        #Google Chrome will know that an automated system is accessing it
        #Python will wait till the webpage is loaded before moving forward
        driver.get(url)

        #Getting title of the video
        try:
            vidTitle.set(driver.find_element_by_css_selector('#container > h1 > yt-formatted-string').text)
            print('TITLE = '+vidTitle)
            root.update_idletasks()
        except Exception as e:
            print(e)

        #Loop to refresh and repeat the whole process
        while (True):
            #Video doesn't seem to autstart
            #So we're checking if the play button is displayed
            try:
                mainPlayButtonOverlay = driver.find_element_by_class_name(
                    'ytp-cued-thumbnail-overlay')
                print('Found Main Play Button Overlay')
            except Exception as e:
                print(e)

            # If the play button is displayed we click on it and autostart the video
            if (mainPlayButtonOverlay.is_displayed()):
                print('Video did not start')
                try:
                    mainPlayButton = driver.find_element_by_css_selector(
                        '#movie_player > div.ytp-cued-thumbnail-overlay > button')
                    print('Found Main Play Button')
                    mainPlayButton.click()
                    print('Started video')
                except Exception as e:
                    print(e)

            #Checking if Advertisement is being displayed
            try:
                adSkipSlot = driver.find_element_by_css_selector(
                    '.ytp-ad-player-overlay-skip-or-preview')
                print('Found Ad Player Overlay')

                #If advertisement is being displayed,
                if (adSkipSlot.is_displayed()):
                    print('Ad is active')
                    while True:
                        try:
                            #Getting the Button slot so we can tell if the button is displayed or not
                            skipButtonSlot = driver.find_elements_by_css_selector(
                                '.ytp-ad-skip-button-slot')
                            print('Found Skip Button Slot')
                            #Checking if button is displayed
                            if (skipButtonSlot[0].is_displayed()):
                                print('Skip button is Active')
                                #We click the skip button
                                try:
                                    skipAd = driver.find_element_by_css_selector(
                                        '.ytp-ad-skip-button.ytp-button')
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
                progressBar = driver.find_element_by_class_name(
                    'ytp-progress-bar ')
                print('Found Progress Bar')
                #Getting Play button
                #Also identies if its a normal video or playlist video
                try:
                    playButton = driver.find_element_by_css_selector(
                        '.ytp-play-button.ytp-button.ytp-play-button-playlist')
                    print('Found Playlist Play Button')
                except Exception as e:
                    #If play button is not a playlist play button
                    print(e)
                    try:
                        playButton = driver.find_element_by_css_selector(
                            '.ytp-play-button.ytp-button')
                        print('Found Play Button')
                        refreshType = 'reload'
                    except Exception as e:
                        print(e)
                

                prevButton = driver.find_element_by_css_selector(
                    '.ytp-prev-button.ytp-button')
                print('Found Prev Button')
                settingsButton = driver.find_element_by_css_selector(
                    '.ytp-button.ytp-settings-button.ytp-hd-quality-badge')
                print('Found Settings Button')
                maxVal = int(progressBar.get_attribute('aria-valuemax'))
                #BACKUP INCASE VIDEO DOESNT PLAY
                playButtonText = playButton.get_attribute('aria-label')
                print('PlayButtonText: ',playButtonText)
                if 'Play' in playButtonText:
                    print('Video is not playing')
                    playButton.click()
                    print('Backup- Play Button Clicked')
                while (True):
                    try:
                        #Opening the settings to make sure progress bar is displayed
                        #Values get updated only as long as progress bar is displayed
                        settingsButton.click()
                        # print()
                    except Exception as e:
                        print(e)
                    currVal = int(progressBar.get_attribute('aria-valuenow'))
                    if (currVal >= maxVal - 1):
                        try:
                            if (refreshType == 'prev'):
                                prevButton.click()
                                print(
                                    '====================Restarted===================='
                                )
                            elif (refreshType == 'reload'):
                                driver.refresh()
                                print(
                                    '====================Restarted===================='
                                )
                                break
                        except Exception as e:
                            print(e)

            except Exception as e:
                print(e)

    #Implementing THREADING to prevent GUI from crashing
    t = threading.Thread(target=mainfunc)
    t.start()


#================================ UI ================================
#root represents the main window
root = tkinter.Tk()
root.title(' YouTube Replay')
root.iconbitmap('assets/YouTubeLogoFavicon.ico')

#Function to open the dialog containing information
def infoDialog():
    popup = Tk()
    popup.title('Information')
    popup.iconbitmap('assets/InfoIconFavicon.ico')
    mainfont = ('','10')
    line1 = Label(popup,text='The SUBMIT button will only be enabled if a valid\nYouTube link has been inserted.\
        \n\nThis program will perform the following tasks:\
        \n-Autostart the video if it hasnt already started\
        \n-Check if Advertisement is being displayed\
        \n-Skip Advertisement once waiting period is over\
        \n-Replay the video once it has reached the end')
    line1.config(font=mainfont,justify=LEFT)
    line1.grid(row=0,column=0,sticky=W,padx=10,pady=5)
    #POSITIONING
    # Apparently a common hack to get the window size. Temporarily hide the
    # window to avoid update_idletasks() drawing the window in the wrong
    # position.
    popup.withdraw()
    popup.update_idletasks()  # Update "requested size" from geometry manager
    x = (popup.winfo_screenwidth() - popup.winfo_reqwidth()) / 2
    y = (popup.winfo_screenheight() - popup.winfo_reqheight()) / 2
    popup.geometry("+%d+%d" % (x, y))
    # This seems to draw the window frame immediately, so only call deiconify()
    # after setting correct window position
    popup.deiconify()
    popup.mainloop()

infoIcon = PhotoImage(file='assets/InfoIcon.png')
# Resizing image to fit on button 
photoimage = infoIcon.subsample(25, 25)

infoBttn = Button(root,command=infoDialog)
infoBttn.config(image=photoimage)

urlLabel = Label(
    root,
    text="Enter the url of the video you would like to play on repeat: ")
urlLabel.config(font=('','15'))

#Function to get the button state
def checkUrl(*args):
    link = strvar.get()
    x = re.search("www.youtube.com",link)
    if(x):
        submitBttn.config(state=NORMAL)
        errLabel.grid_forget()
    else:
        submitBttn.config(state=DISABLED)
        errLabel.grid(row=2,column=0,columnspan=2)

strvar = StringVar(root)
strvar.trace("w", checkUrl)
urlEntry = Entry(root,width=80,textvariable=strvar)
urlEntry.config(font=('','12'))

#Error message
errLabel = Label(root,text="Enter a valid YouTube URL.", fg="red")
errLabel.config(font=('','10'))

#button to submit
submitBttn = tkinter.Button(root,
                            text="SUBMIT",
                            state = DISABLED,
                            command=clickHandle,
                            padx=10,
                            pady=5,
                            )

vidTitle = StringVar(root)

titleLabel = Label(root,text="Video Title: ")
titleLabel.config(font=('','15','bold'))
vidTitleLabel = Label(root,textvariable=vidTitle)
vidTitleLabel.config(font=('','12'))

#GRID LAYOUT
urlLabel.grid(row=0,column=0,padx=5,pady=5,columnspan=2)
urlEntry.grid(row=1,column=0,padx=10,pady=5,columnspan=2)
submitBttn.grid(row=3,column=0,sticky=E,padx=5,pady=5);infoBttn.grid(row=3,column=1,sticky=W,padx=5,pady=5)
titleLabel.grid(row=4,column=0,sticky=E,padx=5,pady=5);vidTitleLabel.grid(row=4,column=1,sticky=W,padx=5,pady=5)

#POSITIONING
# Apparently a common hack to get the window size. Temporarily hide the
# window to avoid update_idletasks() drawing the window in the wrong
# position.
root.withdraw()
root.update_idletasks()  # Update "requested size" from geometry manager
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
# This seems to draw the window frame immediately, so only call deiconify()
# after setting correct window position
root.deiconify()


#this actually launches the UI
root.mainloop()



