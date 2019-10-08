#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# Import all necessary packages for the project.
import os
import time
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver

cwd = os.getcwd()
parentPath = Path(cwd).parent
parentPath = str(parentPath)
# print(parentPath+"\\data")

# this is the setup for selenium
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": parentPath + "\\data",
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(chrome_options=options)  # need to download chromedriver.exe and give path

# In[ ]:

driver.get('http://hansardpublic.parliament.sa.gov.au/#/search/0')  # Hansard website where dates is given for scraping
time.sleep(3)
driver.find_element_by_name('searchstart').clear()
driver.find_element_by_name('searchstart').send_keys("12/02/2019")  # start date for scraping
driver.find_element_by_name('searchend').clear()
driver.find_element_by_name('searchend').send_keys("15/02/2019")  # end date to finish scraping
driver.find_element_by_class_name('hansard-search-button').click()  # it checks search icon in the page after
time.sleep(3)
# this will select only debates from filters in the website present in left side
driver.find_element_by_xpath(("//*[@title=\"Refine by: Answers to Questions\"]")).click()
time.sleep(3)

# In[ ]:

# Scraping all the websites that has debates and storing in the list called allherfs
# note: In this section links of individual xml page is stored
html = driver.page_source.encode("utf-8")  # finding the current page that driver is running
# print (driver.current_url)
soup = BeautifulSoup(html, 'html.parser')  # taking all the html tags from the page
string = "http://hansardpublic.parliament.sa.gov.au/Pages/"  # this string is added later in the extracted href to complete the webpage link of individual xml file
# iteration = 1     Checking the loop status
all_hrefs = []  # list of all links
while soup.findAll("a", title="Move to next page"):  # this will take the page into next page until there is next click icon
    #     print("Iteration:", iteration)
    # looking for all <h3> tags in the page because this tag has links to the xml file of data
    for title in soup.findAll("h3"):
        hrefs = title.findAll("a", href=True)  # looking for all <a> that has href inside it
        if len(hrefs) > 0:
            hrefs = hrefs[0]["href"]
            all_hrefs.append(hrefs)  # appending all links to xml in allHrefs
    time.sleep(4)
    driver.find_element_by_id('PageLinkNext').click()  # this will click the next page icon
    time.sleep(4)
    html = driver.page_source.encode("utf-8")  # this will again grab new link to the website of another page
    soup = BeautifulSoup(html, 'html.parser')
#     iteration = iteration + 1
all_hrefs = [string + s for s in all_hrefs]  # adding string to compete the webpage link
print(all_hrefs)  # websites of individual debates
driver.close()
# all_hrefs contains links of individual xml file page

# In[ ]:

# Scraping all XML files for individual debates
for i in range(len(all_hrefs)):
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(all_hrefs[i])
    driver.find_element_by_xpath("//*[@alt=\"XML\"]").click()  # this will download the xml file
    time.sleep(4)
    driver.close()
