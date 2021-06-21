
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import requests
import time
import re

### News Scraping
# set our news title and paragraph variables (remember, this function will return two values).

def scrape_all():
# set your executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
       
# crezte a function to initiate browser
    news_title, news_paragraph = mars_news(browser)

# Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }
  # Stop webdriver and return data
    browser.quit()
    return data   
# create function
# add an argument to the function
# When we add the word "browser" to our function, 
# we're telling Python that we'll be using the browser variable we defined outside the function
def mars_news(browser):    
# assign the url and instruct the browser to visit it
# Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
# set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

# Add try/except for error handling
    try:
# we've assigned slide_elem as the variable to
# look for the <div /> tag and its descendent 
# (the other tags within the <div /> element
        slide_elem = news_soup.select_one('div.list_text')
# assign the title and summary text to variables we'll reference later. 
# In the next empty cell, let's begin our scraping
# to get just the text,
# Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
   # news_title

# .find() pulls the first one; .find_all() pulls them all
# Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
   # news_p
# Instead of having our title and paragraph printed within the function, we want to return them from the 
# # function so they can be used outside of it. We'll adjust our code to do so by deleting news_title and news_p 
# # and include them in the return statement instead, as shown below.
# add except
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featureds Images Scraping

# set up the URL
# Visit URL
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

# Declare and define our function.
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

# Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

# # An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
# What we've done here is tell BeautifulSoup to look inside the <img /> tag 
# for an image with a class of fancybox-image. Basically we're saying, 
# "This is where the image we want lives—use the link that's inside these tags."

    try:
# Run the notebook cell to see the output of the link.
# Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

    except AttributeError:
        return None
        # add the base URL to our code
# Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url
    return img_url



# ### Scrape Table

# Instead of scraping each row, or the data in each <td />, 
# we're going to scrape the entire table with Pandas' .read_html() function.
# df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] 
# With this line, we're creating a new DataFrame from the HTML table. 
# The Pandas function read_html() specifically searches for and returns a list of 
# tables found in the HTML. By specifying an index of 0, we're telling Pandas to 
# pull only the first table it encounters, or the first item in the list. 
# Then, it turns the table into a DataFrame.
# df.columns=['description', 'Mars', 'Earth'] 
# Here, we assign columns to the new DataFrame for additional clarity.
# df.set_index('description', inplace=True) By using the .set_index() function, 
# we're turning the Description column into the DataFrame's index. inplace=True means 
# that the updated index will remain in place, without having to reassign the DataFrame
# to a new variable. Now, when we call the DataFrame, 
# we're presented with a tidy, Pandas-friendly representation of the HTML 
# table we were just viewing on the website.
def mars_facts():
    # Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
 # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #df

# Pandas also has a way to easily 
# convert our DataFrame back into HTML-ready code using the .to_html() function
# df.to_html()
# Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# end the automated browsing session. 
# This is an important line to add to our web app also. 
# Without it, the automated browser won't know to shut down—it will continue to 
# listen for instructions and use the computer's resources 
# (it may put a strain on memory or a laptop's battery if left on). 
# We really only want the automated browser to remain active while we're scraping data.
 # Stop webdriver and return data




# Hemisphere pictures
# define hemisphere function
def hemispheres(browser):
# add url and browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://marshemispheres.com/'
    browser.visit(url)
 # list to hold the images and titles.
    hemisphere_image_urls = []
# retrieve the image urls and titles for each hemisphere.
    for i in range(4):
    #create empty dictionary
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.find_link_by_text('Sample').first
        img_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    return hemisphere_image_urls

# def scrape_hemisphere(html_text):
#     # parse html text
#     hemi_soup = soup(html_text, "html.parser")
#     # adding try/except for error handling
#     try:
#         title_elem = hemi_soup.find("h2", class_="title").get_text()
#         sample_elem = hemi_soup.find("a", text="Sample").get("href")
#     except AttributeError:
#         # Image error will return None
#         title_elem = None
#         sample_elem = None
#     hemispheres = {
#         "title": title_elem,
#         "img_url": sample_elem
#     }
#     return hemispheres

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())