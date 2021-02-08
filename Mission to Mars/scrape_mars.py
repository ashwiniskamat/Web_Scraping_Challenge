# Import Dependencies / Setup
from bs4 import BeautifulSoup
import os
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def close_browser():
    browser.quit()

def scrape():
    # initialize thedictionary returned by the scrape method for display on the template
    mars_data = {}
    # Scraping using Splinter
    # create a browser instance to be used fro accessing websites and scraping. 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
 
    # Scraping NASA Mars News
    # URL to be scraped. Visit the URL with the browser instance
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    # Use BeautifulSoup to parse out needed information (html)
    html = browser.html
    print(html)
    soup = BeautifulSoup(html,'html.parser')

    # Read the content_title. Skip the first one since it the page title 
    news_titles=[]
    news_title=""
    try:
        news_titles = soup.find_all("div",class_="content_title")
        for xx in news_titles:
            try:
                news_title = xx.text
            except:
                pass
            # Skip this title since it is for the page
            if news_title=="Mars Now":
                continue
            break      
    except Exception as e:
        news_title = "No news is not always good news"
        print(e)

    # retrieve the latest news snippet
    news_paragraph = ""
    try:
        news_paragraph = soup.find("div", class_="article_teaser_body").text.strip()
    except Exception as e:
        print(e)

    # ### Mars Facts 
    # URL to be scraped "https://space-facts.com/mars/"
    facts_url = "https://space-facts.com/mars/"

    # Use pandas to view table contents
    facts_table = pd.read_html(facts_url)
    #facts_table

    facts_df = facts_table[0]
    #facts_df
    facts_df.columns=['Planet', 'Mars']

    # Convert to html
    mars_facts = facts_df.to_html(index=False,index_names=False,classes=["table-bordered", "table-striped", "table-hover", "isi"])
    mars_facts.replace('\n', '')

    # Mars featured image https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    #feature_url = 'https://www.jpl.nasa.gov/news' 
    # the feature website did not work and redirected to the images site

    # Visit website displaying the hemispheres of Mars
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # executable_path = {'executable_path': 'chromedriver'}
    # browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(hemispheres_url)

    # Parse HTML
    html_hemispheres = browser.html
    time.sleep(2)
    soup = BeautifulSoup(html_hemispheres,'html.parser')

    # Pull hemispheres information
    info = soup.find_all('a', class_='itemLink product-item')

    # Start empty list for the URLs
    hemisphere_images_urls = []

    # Loop through the items previously stored
    for i in info: 
        # Store title
        h3_text = ""
        try:
            h3_text =  i.find('h3').text
        except Exception as e:
            print(e)
        # Skip the images without a title to avoid duplicates
        if h3_text == '' :
            continue

        # Store link
        item_link=""
        try:
            item_link = i.get('href')
        except Exception as e:
            print(e)
        # Skip the images without a link
        if item_link == '' :
            continue
        
        # Visit the link that contains the full image website 
        hemispheres_url = f"https://astrogeology.usgs.gov{item_link}"
        browser.visit(hemispheres_url)
        html_hemispheres = browser.html
        time.sleep(1)
        
        # Parse HTML for each individual hemisphere 
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        
        title=""
        try:
            title = soup.find('h2', class_='title').text.strip()
        except Exception as e:
            print(e)
    
        # Get the img
        img_urls=[]
        img_url=""
        try: 
            img_urls = soup.find_all("a", text="Sample")
            for img_link in img_urls:         
                img_url =img_link.get('href')
                break;
        except Exception as e:
            print(e)

        # Retrieve image source 
        # Append the retreived information into a list of dictionaries 
        hemisphere_images_urls.append({"title" : title, "img_url" : img_url})
    # close the browser
    browser.quit()

    #MongoDB
    # Store all scraped data into a dictionary for use by the template
    # Create empty dictionary
    mars_data = {}

    # Add information to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    # Add hemisphere_image_urls to mars_data.
    mars_data['hemisphere_images_urls'] = hemisphere_images_urls

    # Append mars_facts to mars_data.
    mars_data['mars_facts'] = mars_facts

    return mars_data


def main():
    scrape()
if __name__=="__main__":
    main()