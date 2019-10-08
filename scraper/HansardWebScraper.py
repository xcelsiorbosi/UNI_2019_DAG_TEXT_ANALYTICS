# Import all necessary packages for the project.
import pandas as pd
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from functools import reduce
import time
import string
import sys, os
import re
from datetime import datetime
from datetime import timedelta
import logging
def proceedingfilter(directory,xpath,):
    options = webdriver.ChromeOptions()    #option settings
    cwd = os.getcwd()
    options.add_experimental_option("prefs", {
      "download.default_directory": directory,
      "download.prompt_for_download": False,
      "safebrowsing.enabled": True
    })
    end_date = (datetime.today().strftime('%d/%m/%Y'))
    start_date = datetime.today()-timedelta(days=30)
    start_date = (start_date.strftime('%d/%m/%Y'))
    driver = webdriver.Chrome(executable_path='C:\\Users\\Bipin Karki\\Desktop\\chromedriver.exe',chrome_options=options) #need to download chromedriver.exe and give path
    driver.get('http://hansardpublic.parliament.sa.gov.au/#/search/0') #hansard website where dates is given for scraping 
    time.sleep(3)
    driver.find_element_by_name('searchstart').clear()
    driver.find_element_by_name('searchstart').send_keys(start_date)  #start date for scrapping
    driver.find_element_by_name('searchend').clear()
    driver.find_element_by_name('searchend').send_keys(end_date)   #end date to finish scraping
    driver.find_element_by_class_name('hansard-search-button').click() #it clecks search icon in the page after
    time.sleep(3)
    try:
        driver.find_element_by_xpath((xpath)).click() #this will select only debates from filters in the website present in left side
    except NoSuchElementException as exception:
        print ("NO FILES TO DOWNLOAD - please increase the range of date")
        driver.quit()
        sys.exit()
    time.sleep(1)
    #Scraping all the websites that has debates and storing in the list called allherfs
    #note: In this section links of individual xml page is stored
    html = driver.page_source.encode("utf-8")   #finding the current page that driver is running
    #print (driver.current_url)
    soup = BeautifulSoup(html,'html.parser')   #taking all the html tags from the page
    # iteration = 1     Checking the loop status

    allHrefs = []      #list of all links
    
    while soup.findAll("a", title="Move to next page"): #this will take the page into next page until there is next click icon
    #  print("Iteration:", iteration)
        for title in soup.findAll("h3"):                #looking for all <h3> tags in the page because this tag has links to the xml file of data
            hrefs = title.findAll("a", href = True)     #looking for all <a> that has href inside it
            if len(hrefs) > 0:
                hrefs = hrefs[0]["href"]
                allHrefs.append(hrefs)                  #appending all links to xml in allHrefs
        time.sleep(4)
        driver.find_element_by_id('PageLinkNext').click() #this will click the next page icon
        time.sleep(5)
        html = driver.page_source.encode("utf-8")       #this will again grab new link to the website of another page
        soup = BeautifulSoup(html,'html.parser')    
    #     iteration = iteration + 1
    driver.close()
    driver.quit()
    #creating a file name to download
    downloading_filename = []
    for i in allHrefs:
            filename = re.findall('(?<=/docid/).*$', i)
            (downloading_filename).append(filename)
    downloading_filename = reduce(lambda x,y: x+y, downloading_filename)
    filetype = ".xml"
    downloading_filename = [s+filetype for s in downloading_filename]
    print ("\n\nDownload file names to compare with files in directory\n\n\n", downloading_filename)
    print("\nNumber of files queued to download = ",len(downloading_filename))

    #creating a dataframe to compare and drop existing files
    filesindir = os.listdir(directory) #getting file names from directory
    #print("\n\n\nList of files in the directory \n\n\n", filesindir)
    string = "http://hansardpublic.parliament.sa.gov.au/Pages/" #this string is added later in the extracted href to complete the webpage link of individual xml file
    df_allHrefs = pd.DataFrame(allHrefs)
    df_allHrefs['download_file_name'] = downloading_filename
    df_allHrefs = df_allHrefs.drop(df_allHrefs[df_allHrefs.download_file_name.isin(filesindir)].index.tolist())
    allHrefsfile= [string+s for s in df_allHrefs[0]]             #adding string to compete the webpage link
    print("\n\n\n\nLinks of xmls ready to download \n\n\n",allHrefsfile)
    print("\n\n\n\ntotal number of files to be downloaded after filter = ",len(allHrefsfile))
    if len(allHrefsfile) > 0:
        driver = webdriver.Chrome(executable_path='C:\\Users\\Bipin Karki\\Desktop\\chromedriver.exe',chrome_options=options)
        for i in range(len(allHrefsfile)):
            driver.get(allHrefsfile[i])
            driver.find_element_by_xpath(("//*[@alt=\"XML\"]")).click() #this will download the xml file
            time.sleep(5)
        driver.close()
        driver.quit()
    else:
        print("Your directory is up to date")

###### Hansard Bills calls ##########
print("starting Bills")
directoryofBills = ('E:\\hansardbills')                   #Directory of question time files in database
xpathofBills = ("//*[@title=\"Refine by: Bills\"]")        #xpath of all Question time files in Hansard website
proceedingfilter(directoryofBills,xpathofBills)          #passing arguments in function

###### Hansard Question time calls ##########
print("starting QT")
directoryofQT = ('E:\\hansardquestiontime')                #Directory of question time files in database
xpathofQT = ("//*[@title=\"Refine by: Question Time\"]")   #xpath of all Question time files in Hansard website
proceedingfilter(directoryofQT,xpathofQT)                #passing arguments in function

###### Hansard Question and Answer calls ##########
print("starting QANDA")
directoryQnA = ('E:\\hansardqna')                           #Directory of question and answer files in database
xpathofQnA = ("//*[@title=\"Refine by: Answers to Questions\"]")  #xpath of all Question answer files in Hansard website
proceedingfilter(directoryQnA,xpathofQnA)                         #passing arguments in function


