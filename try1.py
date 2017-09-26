# from PIL import Image
# from pytesseract import image_to_string

# print image_to_string(Image.open('https://c22blog.files.wordpress.com/2010/10/input-black.gif'))
# # print image_to_string(Image.open('test-english.jpg'), lang='eng')
import time

import urllib2

import subprocess

from selenium import webdriver

#Create new Selenium driver

driver = webdriver.Firefox()

driver.get(

      "http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200")

time.sleep(2)

#Click on the book preview button

driver.find_element_by_id("sitbLogoImg").click()

imageList = set()

#Wait for the page to load

time.sleep(5)

#While the right arrow is available for clicking, turn through pages

while "pointer" in driver.find_element_by_id("sitbReaderRightPageTurner").get_attribute("style"):

    driver.find_element_by_id("sitbReaderRightPageTurner").click()

    time.sleep(2)

    #Get any new pages that have loaded (multiple pages can load at once,

        #but duplicates will not be added to a set)

    pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")

    print(pages)

    for page in pages:

        image = page.get_attribute("src")

        imageList.add(image)

driver.quit()

print("sdfsdfs")
#Start processing the images we've collected URLs for with Tesseract

print(imageList)

for image in sorted(imageList):

    urllib2.urlretrieve(image, "page.jpg")

    p = subprocess.Popen(["tesseract", "page.jpg", "page"],

                             stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    p.wait()

    f = open("page.txt", "r")

    print(f.read())