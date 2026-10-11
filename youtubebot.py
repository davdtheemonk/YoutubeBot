#This is a youtube Bot that is able to view a video,and eventually add views on youtube videos
#Code cheza kiwewe
#Tested and works on Windows Machine.
"""Author : X
   ©2021 David Mugalla"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
from bs4 import BeautifulSoup
from time import sleep

URL = input("Enter valid URL of Youtube Video  >begin with 'https://' \n ")

logging.basicConfig(filename='Botlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

page  = requests.get(URL)

def viewAction(soup, duration_seconds):
    viewCounter = 0
    ans = input("Is this the video you want to get more views : y or n ? ")
    newViews = int(input("How many views would you like to add? "))
    if (ans=='y'):
        logging.warning("========== Starting Bot Activity ==========")
        
        while(viewCounter<newViews):
            ChromeOptions = Options()
            # Modern headless configuration
            ChromeOptions.add_argument("--headless=new") 
            
            # No executable_path needed; modern Selenium handles this automatically
            browser = webdriver.Chrome(options=ChromeOptions)
            browser.get(URL)
            browser.implicitly_wait(10)
            
            try:
                WebDriverWait(browser,15).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Play']"))).click()
                print("---------------------")
                print("Video has started playing "+ "\U0001F910")
                print("---------------------")
                logging.info("Video has started playing")
                
                # Sleep based on the scraped duration passed into the function
                sleep(duration_seconds)
                
            except Exception as e:
                logging.error(f"Failed to play video or wait timed out: {e}")

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
        exit(-1)


def vidScrapper(page):
    soup = BeautifulSoup(page.content,"html.parser")
    regex = re.compile(r'^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu.be\/))([a-zA-Z0-9\-_])+')

    duration_seconds = 30 # Default safety fallback duration
    
    if regex.match(URL):
        try:
            print("Valid URL\n")
            logging.info("Found information about video")

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
                
            # Internal replacement for pafy: extracts ISO 8601 duration string (e.g., PT4M35S)
            duration_meta = soup.find("meta", itemprop="duration")
            if duration_meta:
                iso_duration = duration_meta['content'] # Example: PT5M12S
                numbers = re.findall(r'\d+', iso_duration)
                if 'H' in iso_duration and 'M' in iso_duration and 'S' in iso_duration:
                    duration_seconds = int(numbers[0])*3600 + int(numbers[1])*60 + int(numbers[2])
                elif 'M' in iso_duration and 'S' in iso_duration:
                    duration_seconds = int(numbers[0])*60 + int(numbers[1])
                elif 'S' in iso_duration:
                    duration_seconds = int(numbers[0])
    
            print("\n     ==============================================      \n")
            
        except Exception as e:
            logging.error(f"An Error occured while finding the video: {e}")
            exit(-1)
    else :
        print("Invalid URL please enter a valid Youtube Video URL")
        exit(-1)
       
    return viewAction(soup, duration_seconds)

if __name__ == "__main__":
    logging.info('Starting program')
    vidScrapper(page)
