from flask import Flask, redirect, url_for, render_template, request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        keyword = request.form['keyword']
        return redirect(url_for('scrape', keyword=keyword))
    return  render_template('home.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    keyword = request.form['keyword']
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-logging")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path='/home/ubuntu/chromedriver', options=options)
    harga, listing, badge, gambar, links = [], [], [], [], []
    for page in range(1, 3):
        driver.get('https://www.etsy.com/search?q={}&page={}&ref=pagination'.format(keyword, page))
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, "html.parser")
        header_contents = soup.find_all('li', 'wt-list-unstyled')
        # time.sleep(sleepTimer)

        for content in header_contents:
            try:
                thumb = content.find('img').get('src')
            except:
                thumb = 'none'
            try:
                product = content.find('h3', 'wt-text-caption v2-listing-card__title wt-text-truncate').text
            except:
                product = 'none'
            try:
                shop = content.find('p', 'wt-text-caption wt-text-truncate wt-text-gray wt-mb-xs-1').text
            except:
                shop = 'none'
            try:
                price = content.find('span', 'currency-value').text
            except:
                price = 'none'
            try:
                sale = content.find('span', 'wt-badge').text
            except:
                sale = '-'
            try:
                link_produk = content.find('div').a.get('href')
            except:
                continue

            listing.append(product)
            harga.append(price)
            badge.append(sale)
            gambar.append(thumb)
            links.append(link_produk)

    return render_template("index.html", len=len(listing), listing=listing, harga=harga, badge=badge, gambar=gambar,
                           links=links,keyword=keyword)

if __name__ == "__main__":
    app.run()