import os
import requests
import smtplib
from bs4 import BeautifulSoup

URL = os.getenv('URL')

def check_price():
    headers = {'User-Agent': os.getenv('USER_AGENT')}

    page = requests.get(URL, headers=headers)

    dirty_soup = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(dirty_soup.prettify(), 'html.parser')

    title = soup.find(id='productTitle').get_text()
    price = soup.find(id='priceblock_ourprice').get_text()
    conv_price = float(price[1:].replace(',',''))

    if conv_price < 1500:
        send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(os.getenv('MAIL_SENDER_EMAIL'), os.getenv('MAIL_SENDER_PASSWORD'))

    subject = 'Price fell down!!'
    body = 'Check the amazon link ' + URL
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        os.getenv('MAIL_SENDER_EMAIL'),
        os.getenv('MAIL_RECIEVER_EMAIL'),
        msg
    )

    print("EMAIL HAS BEEN SENT")
    server.quit()

check_price()
