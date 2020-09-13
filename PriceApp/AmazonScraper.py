from selectorlib import Extractor
import requests
import json
from time import sleep
import smtplib
import time
from background_task import background
import os

cwd = os.getcwd()
files = os.listdir(cwd)
print("Files in %r: %s" % (cwd, files))
# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('./PriceApp/selectors.yml')


def scrape(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)


input_URL = "https://www.amazon.ca/Logitech-Advanced-Wireless-Illuminated-Keyboard/dp/B07S92QBCJ/ref=sr_1_1?dchild=1&keywords=logitech+mx+keys&qid=1598291919&sr=8-1"
input_price = 150
input_email = "guanxianghuang@gmail.com"


# @background(schedule=1)
def check_price(url, price_wanted, email):
    print("inside check_price")
    URL = url
    data = scrape(URL)
    print("DEBUG DATA =")
    print(data)
    price = data["price"]
    print("TYPE OF PRICE IS = ", type(price))
    if price is None:
        print("DEBUUUUUUUUUUUUUUUUUUUUUUUUUUUG")
        return
    price_num = float(price[5:])

    print(data)
    print(price)
    print(price_num)

    if price_num < float(price_wanted):
        send_mail(email, url)


def send_mail(email, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('pricenotification888@gmail.com', '10100701')
    subject = 'New price!'
    body = 'The price for the following product has dropped : ' + url
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('pricenotification888@gmail.com', email, msg)
    print("Email has been sent!")
    server.quit()

# while(True):
#     check_price(input_URL, input_price)
#     time.sleep(86400)
