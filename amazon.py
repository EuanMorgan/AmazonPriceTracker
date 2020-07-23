import requests
from bs4 import BeautifulSoup
import smtplib
import time


items = [["https://www.amazon.co.uk/gp/product/B07SXNDKNM", 139.99],
         ["https://www.amazon.co.uk/gp/product/B078KBKFZ6", 42.98],
         ["https://www.amazon.co.uk/gp/product/B07J2Q4SWZ", 94.49],
         ["https://www.amazon.co.uk/gp/product/B016UPDULO", 67.98]]


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}


def checkPrice():

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    print("Checking price for " + title.strip())
    price = soup.find(id="priceblock_ourprice").get_text()

    if(origPrice > 100):

        conv_price = float(price[1:7])
    else:
        conv_price = float(price[1:6])

    print("Original Price {}\n Current Price: {}".format(origPrice, conv_price))

    if(conv_price < origPrice):
        print("Price dropped!")
        sendMail(title.strip(), URL, origPrice, conv_price)
    else:
        print("No difference")

    # print(title)
    # print(conv_price)


def sendMail(title, URL, original, new):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    password = "PASSWORD HERE"
    server.login('euanmorgan48@gmail.com', password)

    subject = f"Price dropped for {title}"

    body = f"Old Price: {original}\nNew Price: {new}\nDifference: {original - new}\n{URL}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        "euanmorgan48@gmail.com",
        "msboedog@gmail.com",
        msg
    )
    print("Sent email")

    server.quit()


while True:
    print("============================================================================================")
    for i in items:
        URL = i[0]
        origPrice = i[1]
        checkPrice()
    time.sleep(3600)
