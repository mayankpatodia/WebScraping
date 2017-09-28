# WebScraping
Scraping Indian Post to track consignment details
Requires Firefox Browser to be installed

Steps:
1. Install python 3.4

2. Install selenium driver:
	 - Command: $ sudo easy_install selenium
	 - URL: http://damien.co/resources/how-to-install-selenium-2-mac-os-x-python-7391

3. Install geckodriver for Firefox:
	 - Command: brew install geckodriver
	 - URL: http://remarkablemark.org/blog/2016/11/06/selenium-geckodriver/

3. Install BeautifulSoup
	 - Command: $ sudo pip install BeautifulSoup
	 - Command: $ sudo easy_install bs4

4. Install pillow (Python Image Library)
	 - Command: $ sudo pip install pillow
	 - URL:https://wp.stolaf.edu/it/installing-pil-pillow-cimage-on-windows-and-mac/

5. Install tesseract
	 - Command: $ brew install tesseract
	 - Also try $ sudo easy_install pytesseract
	 - URL: https://github.com/tesseract-ocr/tesseract/wiki

6. I don't think you explicitly need to install urllib, but in case you need it,
   Install urllib
	- Command: $ sudo pip install urllib

7. Run the code


Working:
------------------
1. Asks for tracking id as input in te terminal.
2. Opens Firefox Browser.
3. Selenium does the task of enterng the input and fetching the output.
4. Browser closes.
5. Prints the JSON in the terminal as desired.
