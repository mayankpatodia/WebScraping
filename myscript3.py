import requests
from lxml import html

CONSIGNMENT_ID = "RM719962415IN"

LOGIN_URL = "https://www.indiapost.gov.in/VAS/Pages/trackconsignment.aspx"
URL = "https://bitbucket.org/dashboard/repositories"

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)

    # # Create payload
    # payload = {
    #     "username": USERNAME, 
    #     "password": PASSWORD, 
    #     "csrfmiddlewaretoken": authenticity_token
    # }

    # # Perform login
    # result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # # # Scrape url
    # result = session_requests.get(URL, headers = dict(referer = URL))
    # tree = html.fromstring(result.content)
    # bucket_names = tree.xpath("//div[@class='repo-list--repo']/a/text()")

    # print(bucket_names)
    print(result)

if __name__ == '__main__':
    main()