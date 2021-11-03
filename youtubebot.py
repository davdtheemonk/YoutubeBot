#This is a youtube Bot that is able to view a video,and eventuallly add views on youtube videos

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pafy
import requests
import re
from bs4 import BeautifulSoup
from time import sleep

URL = input("Enter valid URL of Youtube Video  >begin with 'https://' \n ")

logging.basicConfig(filename='Botlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

page  = requests.get(URL)


def viewAction(soup):

    
    viewCounter = 0
    ans = input("Is this the video you want to get more views : y or n ? ")
    newViews = int(input("How many views would you like to add? "))
    if (ans=='y'):
        logging.warning("========== Starting Bot Activity ==========")
        
        while(viewCounter<newViews):
            ChromeOptions = Options()
            ChromeOptions.headless = True
            browser = webdriver.Chrome(executable_path=r" ",chrome_options=ChromeOptions)#Your chrome driver goes here
            browser.get(URL)
            browser.implicitly_wait(10)
            #playButton = browser.find_elements_by_xpath("//*[@class='ytp-large-play-button ytp-button']") #For Chrome Users
            #playButton = browser.find_element_by_id("player-container") #For Firefox Users 
            #playButton.click()
            WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Play']"))).click()
            #browser.refresh()#if videos autoplay
            print("---------------------")
            print("Video has started playing "+ "\U0001F910")
            print("---------------------")
            logging.info("Video has started playing")
            #For 100% watchtime
            video = pafy.new(URL)
            time = video.duration#find the duration of the video
            h,m,s = time.split(':')
            h = int(h)
            m = int(m)
            s = int(s)
            if (h!=0):
                sleep(h*60*60)#give time to the bot to view your video
            elif(h==0):
                if(m!=0):
                    sleep(m*60)
            else:
                sleep(s)

            viewCounter+=1
            print("---------------------")
            print("Video has finished playing "+ "\U0001F619")
            print("---------------------")
            print("---------------------")
            print("Added a total of "+ str(viewCounter) + " view(s)")
            print("---------------------")
            browser.close()
            
            if(viewCounter==newViews-1):
                for view in soup.findAll('div',attrs={'class':'watch-main-col'}):
                    finalview = view.find("meta", itemprop="interactionCount")['content']
                    print(f"final view Count : " + finalview + "\n")
                    logging.info("final view Count : " + finalview + "\n")

            
            sleep(2)



    else:
        print("Terminating Activity")
        exit -1


def vidScrapper(page):
    soup = BeautifulSoup(page.content,"html.parser")
    regex = re.compile(r'^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu.be\/))([a-zA-Z0-9\-_])+')

#Finding possible information about the url of the video
    result ={}
    if regex.match(URL):
        try:
            print("Valid URL\n")
            logging.info("Found information about video")

        #Scraps page to find info about the video your requesting

            print("\n     ==============================================      \n")
            for info in soup.findAll('div',attrs={'class':'watch-main-col'}):
                title  = info.find("meta", itemprop="name")["content"]
                print(f"Title of Video : " + title + "\n")
                logging.info(title)

            for date in soup.findAll('div',attrs={'class':'watch-main-col'}):
                date = date.find("meta",itemprop="datePublished")["content"]
                print(f'Date Published :' + date + "\n")
                logging.info('Date :' + date + "\n")
            
    
            for view in soup.findAll('div',attrs={'class':'watch-main-col'}):
                view = view.find("meta", itemprop="interactionCount")['content']
                print(f"Initial view Count : " + view + "\n")
                logging.info("Initial view Count : " + view + "\n")
            
            for desc in soup.findAll('div',attrs={'class':'watch-main-col'}):
                desc = desc.find("meta", itemprop="description")['content']
                print(f"Description : " + desc + "\n")
                logging.info("Description : " + desc + "\n")
    
            print("\n     ==============================================      \n")
            
    
        except:
            logging.error("An Error occured while finding the video")
            exit(-1)
    else :
        print("Invalid URL please enter a valid Youtube Video URL")
        exit(-1)
       
    return viewAction(soup)




    
     

if __name__ == "__main__":
    vidScrapper(page)
    logging.info('Starting program')
    
    