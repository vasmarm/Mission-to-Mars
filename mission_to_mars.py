#Dependencies
import pandas as pd
from splinter import Browser 
from bs4 import BeautifulSoup
import time
from selenium import webdriver


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
# get_ipython().system('which chromedriver')

# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#     return Browser("chrome", **executable_path, headless=False)


def scrape():

    mars_data= {}
    # browser = init_browser()
    # mars_dict = {}
    #import pdb;pdb.set_trace()
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # # NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #News Title
    news_title = soup.find('div', class_="bottom_gradient").text
    print(news_title)
    #Paragraph text
    news_p = soup.find('div', class_='article_teaser_body').text
    # print('--------------------------------------------------')
    print(news_p)

    # Add the news title and summary to the dictionary
    mars_data["news_title"] = news_title
    mars_data["new_p"] = news_p


    # # Featured Image
    #import pdb; pdb.set_trace()
    Image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(Image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    # Extracting image
    Image_path= soup.find('figure',class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov/'+ Image_path
    print(featured_image_url)

    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url



    # # Mars Weather
    mars_tweet = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_tweet)

    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    # Extracting tweet
    mars_weather = soup.find('div',class_='js-tweet-text-container').text.replace('\n','')
    print(mars_weather)

    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather


    # #  Mars Facts
    mars_fact='https://space-facts.com/mars/'
    browser.visit(mars_fact)

    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    # Extracting mars table
    #set up lists to hold td elements which alternate between label and value
    trs=soup.find_all('tr')
    #set up lists to hold td elements which alternate between label and value
    labels = []
    values = []

    #for each tr element append the first td element to labels and the second to values
    for tr in trs:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
    print(labels,values)

    mars_fact_tabel = pd.DataFrame({
        "Label": labels,
        "Values": values
    })
    #mars_fact_tabel

    # convert the data to a HTML table string
    fact_table = mars_fact_tabel.to_html(header = False, index = False)
    print(fact_table)

    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = fact_table



    # # Mars Hemispheres
    USGS_site= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(USGS_site)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')

    # Get the div element that holds the images. 
    images = soup.find('div', class_='collapsible results')
    #Loop through the class="item" by clicking the h3 tag and getting the title and url. 

    hemispheres_image_urls = []

    # print(len(images.find_all("div", class_="item")))
    for i in range(len(images.find_all("div", class_="item"))):
        # print(i)
        time.sleep(5)
        image = browser.find_by_tag('h3')
        image[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("h2", class_="title").text
        # print(title)
        div = soup.find("div", class_="downloads")
        # for li in div:
        link = div.find('a')
        # print(link)
        url = link.attrs['href']
        
        # print(url)
        hemispheres = {
                'title' : title,
                'img_url' : url
            }
        hemispheres_image_urls.append(hemispheres)
        browser.back()
        
        print(hemispheres_image_urls)

        # Add the hemispheres data to the  dictionary
        mars_data["hemispheres_image_urls"] = hemispheres_image_urls

    # Return the dictionary
    return mars_data

  
        
# Test Scrape_mars
if __name__ == "__main__":
    scrape()