#!/usr/bin/env python

from flask import Flask, jsonify
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from pymongo import MongoClient

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url="https://marshemispheres.com/"
    browser.visit(url)
    homepage_html = browser.html
    soup = bs(homepage_html, 'html.parser')
    div_results = soup.find_all('div', {"class": "item"})
    hemisphere_image_urls = []
    for div_result in div_results:
        item_dict = {}
        asoup = bs(str(div_result), 'html.parser')
        endpoint = asoup.find('a')['href']
        
        browser.visit(url + endpoint)
        soup = bs(browser.html)
        image_endpoint = soup.find("img", {"class": "wide-image"})['src']
        title_endpoint = soup.find("h2", {"class": "title"}).text


        item_dict['title'] = url + image_endpoint
        item_dict['img_url'] = url + title_endpoint
        hemisphere_image_urls.append(item_dict)
    return hemisphere_image_urls
    

