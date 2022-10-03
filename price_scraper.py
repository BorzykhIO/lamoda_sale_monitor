import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import ssl
import smtplib
import time

url = input('Insert link for your product: ')


def get_brand(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    brand_name = soup.find_all("span", {"class": "x-premium-product-title__brand-name"})
    brand_name = brand_name[0].get_text().strip()
    return brand_name


def get_model(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    model_name = soup.find_all("div", {"class": "x-premium-product-title__model-name"})
    model_name = model_name[0].get_text().strip()
    return model_name


def get_price(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all("span", {"class": "x-premium-product-prices__price"})
    try:
        current_price = prices[1].get_text()
        current_price = int(current_price.replace(' ', '').replace('₽', ''))
    except:
        current_price = prices[0].get_text()
        current_price = int(current_price.replace(' ', '').replace('₽', ''))
    return current_price


def compose_email(price_1):
    email_sender = 'ivan4borzyh@gmail.com'
    email_password = 'your passord here'
    email_reciever = 'ivan2borzyh@gmail.com'
    subject = f'{get_brand(url)} {get_model(url)} IS ON SALE!'
    body = f'Hey! \ {get_brand(url)} {get_model(url)} is on sale! \n' \
           f'New price is {price_1} rub! \nGet your product here: {url}'
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())


price_history = {'brand': [get_brand(url)], 'model': [get_model(url)], 'price': [get_price(url)]}
i = 0
while True:
    act_price = get_price(url)
    if act_price > price_history['price'][-1]:
        compose_email(act_price)
        price_history['model'].append(get_model(url))
        price_history['brand'].append(get_brand(url))
        price_history['price'].append(act_price)

    else:
        price_history['model'].append(get_model(url))
        price_history['brand'].append(get_brand(url))
        price_history['price'].append(act_price)
    time.sleep(60 * 60)

