import pandas as pd
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
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": 'C:\\Users\\student\\Desktop\\SSIS Related- Re Moe\\hansard_debates_Q&A-1Year\\QA',
  "download.prompt_for_download": False,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome(executable_path='C:\\Users\\student\\Desktop\\Scraping_Codes_and_ChromeDriver\\chromedriver.exe',chrome_options=options)
driver.get('http://hansardpublic.parliament.sa.gov.au/#/search/0') 
time.sleep(3)
driver.find_element_by_name('searchstart').clear()
driver.find_element_by_name('searchstart').send_keys("01/09/2019")
driver.find_element_by_name('searchend').clear()
driver.find_element_by_name('searchend').send_keys("28/09/2019")
driver.find_element_by_class_name('hansard-search-button').click()
time.sleep(3)
driver.find_element_by_xpath(("//*[@title=\"Refine by: Answers to Questions\"]")).click()
time.sleep(3)
html = driver.page_source.encode("utf-8")
soup = BeautifulSoup(html,'html.parser')
string = "http://hansardpublic.parliament.sa.gov.au/Pages/"
allHrefs = []
while soup.findAll("a", title="Move to next page"):
    for title in soup.findAll("h3"):
        hrefs = title.findAll("a", href = True)
        if len(hrefs) > 0:
            hrefs = hrefs[0]["href"]
            allHrefs.append(hrefs)
    time.sleep(4)
    driver.find_element_by_id('PageLinkNext').click()
    time.sleep(10)
    html = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(html,'html.parser')    
allHrefs= [string+s for s in allHrefs]
print (allHrefs)
driver.close()
for i in range(len(allHrefs)):
    driver = webdriver.Chrome(executable_path='C:\\Users\\student\\Desktop\\Scraping_Codes_and_ChromeDriver\\chromedriver.exe',chrome_options=options)
    driver.get(allHrefs[i])
    driver.find_element_by_xpath(("//*[@alt=\"XML\"]")).click()
    time.sleep(10)
    driver.close()
