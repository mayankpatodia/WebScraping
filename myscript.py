# import libraries
import urllib2
import mechanize
from bs4 import BeautifulSoup

# # specify the url
# quote_page = 'http://www.bloomberg.com/quote/SPX:IND'

# # query the website and return the html to the variable 'page'
# page = urllib2.urlopen(quote_page)

# # parse the html using beautiful soap and store in variable `soup`
# soup = BeautifulSoup(page, 'html.parser')

# # Take out the <div> of name and get its value
# name_box = soup.find('h1', attrs={'class': 'name'})

# name = name_box.text.strip() # strip() is used to remove starting and trailing
# print(name)

# # get the index price
# price_box = soup.find('div', attrs={'class': 'price'})
# price = price_box.text
# print(price)

# soup = BeautifulSoup(response.get_data())
# img = soup.find('img', id='ctl00_SPWebPartManager1_g_d6d774b9_498e_4de6_8690_a93e944cbeed_ctl00_imgCaptcha')
# image_response = browser.open_novisit(img['src'])
# image = image_response.read()# print(browser.response().read())
# print(image)


browser = mechanize.Browser()
br = browser.open("https://www.indiapost.gov.in/VAS/Pages/trackconsignment.aspx")
print(browser.response().read())
browser.select_form(nr=0)
browser['ctl00$SPWebPartManager1$g_d6d774b9_498e_4de6_8690_a93e944cbeed$ctl00$txtOrignlPgTranNo'] = 'RM719962415IN'

