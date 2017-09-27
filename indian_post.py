#Importing all the necessary modules
from selenium import webdriver
from bs4 import BeautifulSoup

import urllib2
import urllib

from PIL import Image
from PIL import ImageOps
import pytesseract
import os

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import json
import datetime
from collections import OrderedDict

#Class with all the functions
class IndianPostScraper(object):
    def __init__(self):
        #Create profile for untrusted certificate
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        
        #Set the url start the driver.
        self.url = "https://www.indiapost.gov.in/VAS/Pages/trackconsignment.aspx"
        self.driver = webdriver.Firefox(firefox_profile=profile)
        self.driver.set_window_size(1120, 550)

        #initialize the final output object
        self.res = OrderedDict({})

    #method for cleaning the image
    def cleanImage(self, imagePath):
        image = Image.open(imagePath)
        image = image.point(lambda x: 0 if x<143 else 255)
        borderImage = ImageOps.expand(image)
        borderImage.save(imagePath)

    #getting the Captcha text from captcha image
    def getCaptha(self, captchaUrl):
        urllib.urlretrieve(captchaUrl, "captcha.gif")
        # print("URL: " + captchaUrl)
        captcha_path = os.getcwd() + "\\captcha.gif"
        # print("PATH: " + captcha_path)
        self.cleanImage("captcha.gif")

        text = pytesseract.image_to_string(Image.open(captcha_path))
        return text

    #main scraping method. Crawls through the website to find the desired data
    def scrape(self):
        cons_id = "RM719962415IN"

        flag = True
        #Loop until we get the correct captcha
        while flag:
            #Start the driver
            self.driver.get(self.url)
            self.driver.wait = WebDriverWait(self.driver, 5)
            
            #Get the form fields
            captcha_image = self.driver.find_element_by_id("ctl00_SPWebPartManager1_g_d6d774b9_498e_4de6_8690_a93e944cbeed_ctl00_imgCaptcha")
            consignment_id_box = self.driver.find_element_by_xpath("/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div/div/div/div/div[1]/div[1]/div[2]/input")
            captcha_box = self.driver.find_element_by_name("ctl00$SPWebPartManager1$g_d6d774b9_498e_4de6_8690_a93e944cbeed$ctl00$txtCaptcha")

            #Get the src of tht captcha image and get Captcha
            captcha_src = captcha_image.get_attribute("src")
            captcha_text = self.getCaptha(captcha_src)
            
            #Set the values in the form
            consignment_id_box.send_keys(cons_id)
            captcha_box.send_keys(captcha_text)

            #Submit the form to search
            self.driver.find_element_by_name('ctl00$SPWebPartManager1$g_d6d774b9_498e_4de6_8690_a93e944cbeed$ctl00$btnSearch').click()
            self.driver.wait = WebDriverWait(self.driver, 5)
            try:
                #If data is correct and the table is shown
                myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[2]')))

                #Fetch data from desired fields
                ship_date = self.driver.find_element_by_xpath('/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[2]').text
                status = self.driver.find_element_by_xpath('/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[4]').text

                if status == "Item delivered":
                    delivery_date = self.driver.find_element_by_xpath('/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[7]').text
                else:
                    delivery_date = 'unavailable'
                
                #Get days from shipping and delivery dates fetched
                ship_day = datetime.datetime.strptime(ship_date, "%d/%m/%Y").strftime('%A')
                delivery_day = datetime.datetime.strptime(delivery_date, "%d/%m/%Y").strftime('%A')

                #Add#Add fetched data to the object
                self.res['cons_id'] = cons_id
                self.res['ship_date'] = ship_day[:3] + " " + ship_date
                self.res['status'] = status
                self.res['delivery_date'] = delivery_day[:3] + " " + delivery_date

                #Print the formatted JSON Object
                print(json.dumps(self.res, indent=4, sort_keys=False))
                break                    
            except NoSuchElementException:
                #If Element Not Found
                print('Element Not Found')
            except TimeoutException:
                #If data incorrect
                print('Incorrect Data. Trying again')
        self.driver.quit()

if __name__ == '__main__':
    #Create the Scraper Object
    scraper = IndianPostScraper()

    #Call the scraper method
    scraper.scrape()        
