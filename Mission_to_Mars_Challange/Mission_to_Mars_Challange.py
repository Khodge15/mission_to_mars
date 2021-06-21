#!/usr/bin/env python
# coding: utf-8

# ### Article Scraping

# In[7]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
import re


# In[8]:


# set your executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[9]:


# assign the url and instruct the browser to visit it
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[10]:


# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
# we've assigned slide_elem as the variable to
# look for the <div /> tag and its descendent 
# (the other tags within the <div /> element
slide_elem = news_soup.select_one('div.list_text')


# In[11]:


# assign the title and summary text to variables we'll reference later. 
# In the next empty cell, let's begin our scraping
slide_elem.find('div', class_='content_title')


# In[12]:


# to get just the text,
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[13]:


# .find() pulls the first one; .find_all() pulls them all
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featureds Images Scraping

# In[14]:


# set up the URL
# Visit URL
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://spaceimages-mars.com'
browser.visit(url)
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[15]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[16]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[17]:


# # An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
# What we've done here is tell BeautifulSoup to look inside the <img /> tag 
# for an image with a class of fancybox-image. Basically we're saying, 
# "This is where the image we want lives—use the link that's inside these tags."

# Run the notebook cell to see the output of the link.
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[18]:


# add the base URL to our code
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scrape Table

# In[19]:


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

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[20]:


# Pandas also has a way to easily 
# convert our DataFrame back into HTML-ready code using the .to_html() function

df.to_html()


# In[21]:


# end the automated browsing session. 
# This is an important line to add to our web app also. 
# Without it, the automated browser won't know to shut down—it will continue to 
# listen for instructions and use the computer's resources 
# (it may put a strain on memory or a laptop's battery if left on). 
# We really only want the automated browser to remain active while we're scraping data.
browser.quit()


# ### Visit the NASA Mars News Site¶

# In[23]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[24]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[25]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[26]:


slide_elem.find('div', class_='content_title')


# In[27]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[28]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[29]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[30]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[31]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[32]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[33]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[34]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[35]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[36]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[40]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[41]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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


# In[42]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[43]:


# 5. Quit the browser
browser.quit()


# In[ ]:




