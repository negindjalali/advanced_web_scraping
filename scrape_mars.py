from pandas.core.accessor import register_series_accessor
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
from time import sleep

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)






def scrape():
    # scrape the news title and paragraph
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    news_title = soup.find_all('div', class_='content_title')[1].get_text()
    
    news_paragraph = soup.find('div', class_='article_teaser_body').get_text()
    

    
    
    # scrape the featured image url
    img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(img_url)
    sleep(2)
    img_html = browser.html
    soup = BeautifulSoup(img_html, 'html.parser')
    body = soup.find_all("body")
    div = body[0].find("div", class_="floating_text_area")
    image = div.find("a")
    pic_source = []
    pic = image['href']
    pic_source.append(pic)
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + pic
    


    # scrape the table
    mars_fact_url = 'https://space-facts.com/mars/'
    sleep(2)
    table = pd.read_html(mars_fact_url)
    facts_df = table[0]
    facts_df.columns=["Description", "Mars"]
    mars_facts = facts_df.to_html()
    
    
    

    
   
    # scrape the hemispheres
    hemisphere_image_urls ="https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"

    response = requests.get(hemisphere_image_urls)
    sleep(2)
    soup = BeautifulSoup(response.text, "html.parser")
    pic = soup.find_all( "div", class_ = "wide-image-wrapper")
    image = pic[0].find("li")
    image_url = image.find("a")['href']
    hemisphere_title = soup.find("h2", class_="title").text

    hemisphere_image_urls_2 ="https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    sleep(2)
    response_2 = requests.get(hemisphere_image_urls_2)
    soup_2 = BeautifulSoup(response_2.text, "html.parser")
    pic_2 = soup_2.find_all( "div", class_ = "wide-image-wrapper")
    image_2 = pic_2[0].find("li")
    image_url_2 = image_2.find("a")['href']
    hemisphere_title_2 = soup_2.find("h2", class_="title").text

    hemisphere_image_urls_3="https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    sleep(2)
    response_3 = requests.get(hemisphere_image_urls_3)
    soup_3 = BeautifulSoup(response_3.text, "html.parser")
    pic_3 = soup_3.find_all( "div", class_ = "wide-image-wrapper")
    image_3 = pic_3[0].find("li")
    image_url_3 = image_3.find("a")['href']
    hemisphere_title_3 = soup_3.find("h2", class_="title").text

    hemisphere_image_urls_4="https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    sleep(2)
    response_4 = requests.get(hemisphere_image_urls_4)
    soup_4 = BeautifulSoup(response_4.text, "html.parser")
    pic_4 = soup_4.find_all( "div", class_ = "wide-image-wrapper")
    image_4 = pic_4[0].find("li")
    image_url_4 = image_4.find("a")['href']
    hemisphere_title_4 = soup_4.find("h2", class_="title").text

    hemisphere= (
    {"title":hemisphere_title, "image_url":image_url},
    {"title":hemisphere_title_2, "image_url":image_url_2},
    {"title":hemisphere_title_3, "image_url":image_url_3},
    {"title":hemisphere_title_4, "image_url":image_url_4},
    )

    # import into a dictionary
    mars_data= { "news_title" : news_title,
                "news_paragraph" : news_paragraph,
                "featured_image_url": featured_image_url,
                "mars_facts": mars_facts,
                "hemisphere_image_urls" : hemisphere
}
    browser.quit()

    return mars_data

if __name__ == "__main__":
    result = scrape()
    print(result)