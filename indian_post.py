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

class IndianPostScraper(object):
    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True


        self.url = "https://www.indiapost.gov.in/VAS/Pages/trackconsignment.aspx"
        self.driver = webdriver.Firefox(firefox_profile=profile)
        self.driver.set_window_size(1120, 550)
        self.res = OrderedDict({})

    def cleanImage(self, imagePath):
        image = Image.open(imagePath)
        image = image.point(lambda x: 0 if x<143 else 255)
        borderImage = ImageOps.expand(image)
        borderImage.save(imagePath)


    def getCaptha(self, captchaUrl):
        urllib.urlretrieve(captchaUrl, "captcha.gif")
        # print("URL: " + captchaUrl)
        captcha_path = os.getcwd() + "\\captcha.gif"
        # print("PATH: " + captcha_path)
        self.cleanImage("captcha.gif")

        text = pytesseract.image_to_string(Image.open(captcha_path))
        return text

    def scrape(self):
        cons_id = "RM719962415IN"

        flag = True
        while flag:
            self.driver.get(self.url)
            self.driver.wait = WebDriverWait(self.driver, 5)
            
            captcha_image = self.driver.find_element_by_id("ctl00_SPWebPartManager1_g_d6d774b9_498e_4de6_8690_a93e944cbeed_ctl00_imgCaptcha")
            consignment_id_box = self.driver.find_element_by_xpath("/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div/div/div/div/div[1]/div[1]/div[2]/input")

            captcha_box = self.driver.find_element_by_name("ctl00$SPWebPartManager1$g_d6d774b9_498e_4de6_8690_a93e944cbeed$ctl00$txtCaptcha")
            captcha_src = captcha_image.get_attribute("src")

            captcha_text = self.getCaptha(captcha_src)
            
            consignment_id_box.send_keys(cons_id)
            captcha_box.send_keys(captcha_text)

            self.driver.find_element_by_name('ctl00$SPWebPartManager1$g_d6d774b9_498e_4de6_8690_a93e944cbeed$ctl00$btnSearch').click()
            self.driver.wait = WebDriverWait(self.driver, 5)
            try:
                myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[2]')))
                ship_date = self.driver.find_element_by_xpath('/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[2]').text
                status = self.driver.find_element_by_xpath('/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[4]').text
                if status == "Item delivered":
                    delivery_date = self.driver.find_element_by_xpath('/html/body/form/div[4]/div/div/div[2]/span/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/section/div/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[7]').text
                else:
                    delivery_date = 'unavailable'
                
                ship_day = datetime.datetime.strptime(ship_date, "%d/%m/%Y").strftime('%A')
                delivery_day = datetime.datetime.strptime(delivery_date, "%d/%m/%Y").strftime('%A')

                self.res['cons_id'] = cons_id
                self.res['ship_date'] = ship_day[:3] + " " + ship_date
                self.res['status'] = status
                self.res['delivery_date'] = delivery_day[:3] + " " + delivery_date

                # data = '{"tracking_id": "' + cons_id + '","ship_date": "' + ship_date + ':,"'
                print(json.dumps(self.res, indent=4, sort_keys=False))
                break                    
            except NoSuchElementException:
                print('Element Not Found')
            except TimeoutException:
                print('Incorrect Data. Trying again')
        self.driver.quit()

if __name__ == '__main__':
    scraper = IndianPostScraper()
    scraper.scrape()        
