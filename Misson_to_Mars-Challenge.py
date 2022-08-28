#!/usr/bin/env python
# coding: utf-8

# ### ARTICLE SCRAPING 

# In[135]:


import pandas as pd


# In[136]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[137]:


#set your executable path in the next cell, 
# then set up the URL (NASA Mars News (Links to an external site.)) for scraping.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[138]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[139]:


#set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[140]:


#assign the title and summary text to variables we'll reference later.
slide_elem.find('div', class_='content_title')


# In[141]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[142]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## JPL Space Images Featured Image

# In[143]:


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# In[144]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[145]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[146]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
print(url+img_url_rel)
img_url_rel


# In[147]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
print(img_url)


# # Mars Facts

# In[148]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[149]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[150]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[153]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
links = browser.find_by_css("a.product-item img")
# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(len(links)):
    hemisphere = {}
    browser.find_by_css("a.product-item img")[i].click()
    sample = browser.links.find_by_text("Sample").first
    hemisphere["img_url"] = sample["href"]
    hemisphere["title"] = browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemisphere)
    browser.back()


# In[154]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[155]:


# 5. Quit the browser
browser.quit()

