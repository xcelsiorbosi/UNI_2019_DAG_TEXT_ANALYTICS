#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import all necessary packages for the project.
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import string
import sys, os
cwd = os.getcwd()

from pathlib import Path
parentPath = Path(cwd).parent
parentPath = str(parentPath)
# print(parentPath+"\\Data")

#this is the setup for silenium
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": parentPath+"\\Data",
  "download.prompt_for_download": False,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome(chrome_options=options) #need to download chromedriver.exe and give path


# In[ ]:


driver.get('http://hansardpublic.parliament.sa.gov.au/#/search/0') #hansard website where dates is given for scraping 
time.sleep(3)
driver.find_element_by_name('searchstart').clear()
driver.find_element_by_name('searchstart').send_keys("12/02/2019")  #start date for scrapping
driver.find_element_by_name('searchend').clear()
driver.find_element_by_name('searchend').send_keys("15/02/2019")   #end date to finish scraping
driver.find_element_by_class_name('hansard-search-button').click() #it clecks search icon in the page after
time.sleep(3)
driver.find_element_by_xpath(("//*[@title=\"Refine by: Answers to Questions\"]")).click() #this will select only debates from filters in the website present in left side
time.sleep(3)


# In[ ]:


#Scraping all the websites that has debates and storing in the list called allherfs
#note: In this section links of individual xml page is stored
html = driver.page_source.encode("utf-8")   #finding the current page that driver is running
#print (driver.current_url)
soup = BeautifulSoup(html,'html.parser')   #taking all the html tags from the page
string = "http://hansardpublic.parliament.sa.gov.au/Pages/" #this string is added later in the extracted href to complete the webpage link of individual xml file
# iteration = 1     Checking the loop status
allHrefs = []      #list of all links
while soup.findAll("a", title="Move to next page"): #this will take the page into next page until there is next click icon
#     print("Iteration:", iteration)
    for title in soup.findAll("h3"):                #looking for all <h3> tags in the page because this tag has links to the xml file of data
        hrefs = title.findAll("a", href = True)     #looking for all <a> that has href inside it
        if len(hrefs) > 0:
            hrefs = hrefs[0]["href"]
            allHrefs.append(hrefs)                  #appending all links to xml in allHrefs
    time.sleep(4)
    driver.find_element_by_id('PageLinkNext').click() #this will click the next page icon
    time.sleep(4)
    html = driver.page_source.encode("utf-8")       #this will again grab new link to the website of another page
    soup = BeautifulSoup(html,'html.parser')    
#     iteration = iteration + 1
allHrefs= [string+s for s in allHrefs]             #adding string to compete the webpage link
print (allHrefs)   #websites of individual debates  
driver.close()
#allHrefs contains links of individual xml file page


# In[ ]:


#Scrapping all XML files for individual debates
for i in range(len(allHrefs)):
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(allHrefs[i])
    driver.find_element_by_xpath(("//*[@alt=\"XML\"]")).click()    #this will download the xml file
    time.sleep(4)
    driver.close()

