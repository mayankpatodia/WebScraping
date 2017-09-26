# from PIL import Image
# from pytesseract import image_to_string

# print image_to_string(Image.open('https://c22blog.files.wordpress.com/2010/10/input-black.gif'))
# # print image_to_string(Image.open('test-english.jpg'), lang='eng')
import time
import urllib2
import urllib
import subprocess
from selenium import webdriver
from bs4 import BeautifulSoup
import subprocess
from PIL import Image
from PIL import ImageOps
import pytesseract
import os

#Create new Selenium driver

def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x<143 else 255)
    borderImage = ImageOps.expand(image,border=20,fill='white')

    borderImage.save(imagePath)


html = urllib2.urlopen("http://www.pythonscraping.com/humans-only")

bsObj = BeautifulSoup(html)

#Gather prepopulated form values

imageLocation = bsObj.find("img", {"title": "Image CAPTCHA"})["src"]

formBuildId = bsObj.find("input", {"name":"form_build_id"})["value"]

captchaSid = bsObj.find("input", {"name":"captcha_sid"})["value"]

captchaToken = bsObj.find("input", {"name":"captcha_token"})["value"]

captchaUrl = "http://pythonscraping.com"+imageLocation

urllib.urlretrieve(captchaUrl, "captcha.jpg")
print(captchaUrl)


cleanImage("captcha.jpg")


# p = subprocess.Popen(["tesseract", "captcha.jpg", "captcha"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# p.wait()
captcha_path = os.getcwd() + "\\captcha.jpg"
print(captcha_path)
text = pytesseract.image_to_string(Image.open(captcha_path))
print(text)

f = open("captcha.txt", "r")

#Clean any whitespace characters

captchaResponse = f.read().replace(" ", "").replace("\n", "")

print("Captcha solution attempt: "+captchaResponse)

if len(captchaResponse) == 5:

    params = {"captcha_token":captchaToken, "captcha_sid":captchaSid,  

              "form_id":"comment_node_page_form", "form_build_id": formBuildId,

                  "captcha_response":captchaResponse, "name":"Ryan Mitchell",

                  "subject": "I come to seek the Grail",

                  "comment_body[und][0][value]":

                                           "...and I am definitely not a bot"}

    r = urllib2.requests.post("http://www.pythonscraping.com/comment/reply/10",

                          data=params)

    responseObj = BeautifulSoup(r.text)

    if responseObj.find("div", {"class":"messages"}) is not None:

        print(responseObj.find("div", {"class":"messages"}).get_text())

else:

    print("There was a problem reading the CAPTCHA correctly!")