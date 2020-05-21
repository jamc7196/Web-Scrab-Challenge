# Student Jorge Alberto Muñozcano Castro: Web Scrape Challenge Part2 
# import Dependencies 
# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import pymongo
import pandas as pd
import requests as req
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scraper():
#1)Nasa Mars
    browser = init_browser()

    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url) 
    html = browser.html 
    nasasoup = bs(html, "html.parser")
    article = nasasoup.find("div", class_='list_text')
    maintitle = article.find("div", class_="content_title").text
    newspara= article.find("div", class_ ="article_teaser_body").text
#2)JPL Image
    # Establish link with url: Latest NewsJPL Featured Space Image
    nasaimage = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasaimage) #test succesfull, link established
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    jplsoup = bs(html, 'html.parser')
    jpl_img_url = jplsoup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{jpl_img_url}'
#3)Mars Weather Twitter
    lastupdate = req.get("https://twitter.com/marswxreport?lang=en")
    twittersoup2 = bs(lastupdate.text, 'html.parser')
    twitteracount = twittersoup2.find_all('div', class_="js-tweet-text-container")
    for tweets in twitteracount:
        if tweets.text:
            print(tweets.text)
            break     
#4) Mars Facts
    marsfacts = "https://space-facts.com/mars/"
    browser.visit(marsfacts)
    html = browser.html
    mars_table = pd.read_html(marsfacts)
    #table 1
    mars_facts1 = mars_table[0]
    mars_facts1 
    mars_facts1.rename(columns={0: 'Mars Description', 1: 'Mars Value'}) 
    marsft1_html = mars_facts1.to_html()
    marsft1_html
    #table 2
    mars_facts2 = mars_table[1]
    mars_facts2
    marsfacts2=mars_facts2[["Mars - Earth Comparison", "Mars"]]
    marsfacts2
    mars_facts2=marsfacts2.rename(columns={'Mars - Earth Comparison': 'Mars Description', 'Mars': 'Mars Value'})
    marsft2_html = mars_facts2.to_html()
    marsft2_html
#5) Mars Hemispheres
    usgastraimg="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    short_usgas="https://astrogeology.usgs.gov"
    browser.visit(usgastraimg) 
    html = browser.html
    linksoup = bs(html , 'html.parser')
    main_link = linksoup.find_all('div', class_='item')
    hemisphere_img_links=[]
    #Using the function find all from Beautiful soup scrap the main link

    for link in main_link:
        title = link.find('h3').text
        astrolink = link.find('a')['href']
        hem_img_link= short_usgas+astrolink
        browser.visit(hem_img_link)
        html = browser.html
        hemisoup = bs(html, 'html.parser')
        hemisphere_original= hemisoup.find('div',class_='downloads')
        hemisphere_img_link=hemisphere_original.find('a')['href']
        print(hemisphere_img_link)
        astro_image=dict({'title':title, 'img_url':hemisphere_img_link})
        hemisphere_img_links.append(astro_image) 
        hemisphere_img_links

        # Store data in a dictionary
        mars_data = {
            "news_title": maintitle,
            "news_p": newspara,
            "featured_image_url": featured_image_url,
            "mars_weather": tweets.text,
            "mars_facts1": marsft1_html,
            "mars_facts2": marsft2_html,
            "hemisphere_image_urls": hemisphere_img_links
        }
        # Close the browser after scraping
        browser.quit()
        # Return results
        return mars_data

if __name__ == '__main__':
    scraper()



