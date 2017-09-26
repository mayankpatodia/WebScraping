from PIL import Image
from PIL import ImageEnhance
import pytesseract
import urllib
import cStringIO

url = "https://c22blog.files.wordpress.com/2010/10/input-black.gif"
file = cStringIO.StringIO(urllib.urlopen(url).read())
# Opening the image along with specific path.
image  = Image.open(file)
# Converting the image to string.
text_data = pytesseract.image_to_string(file)
text_data = pytesseract.image_to_string(file, graceful_errors=True)
# Writing the string data to a text file. 
text_file = open(text_file_path, "w+")
text_file.write("%s" % text_data)
text_file.close()