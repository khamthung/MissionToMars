from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():

    browser = init_browser()
    # NASA Mars News
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    imgurl = soup.find('article', class_='carousel_item').get('style')
    img_src = imgurl.split("'")[1]
    featured_image_url=f"https://www.jpl.nasa.gov{img_src}"
    
    #Mars Weather
    url="https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    mars_weather =soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.split("https")[0]

    
    #Mars Facts
    url="https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description',inplace=True)
    mars_html_table = df.to_html().replace('\n', '')

    
    #Mars Hemispheres
    hemisphere_image_urls =[]
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items=soup.find("div",class_="collapsible results").find_all('div',class_="item")

    for item in items:
        title=item.find("img", class_="thumb").get("alt").split(" thumbnail")[0]
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find("div", class_="downloads").find("ul").find("li").a.get("href")
        hemisphere_image_urls.append({"title":title, "img_url":img_url })
        browser.back()

    browser.quit()
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather":mars_weather,
        "facts":mars_html_table,
        "hemispheres":hemisphere_image_urls
    }

    # Return results
    return mars_data
