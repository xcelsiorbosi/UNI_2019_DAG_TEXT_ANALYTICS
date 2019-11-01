# Import all necessary packages for the project.
import configparser
import os
import re
import sys
import time
from datetime import datetime
from datetime import timedelta
from functools import reduce

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def proceeding_filter(directory, xpath):

    # Read required values from projects configuration file
    config = configparser.ConfigParser()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '..\\config.ini')
    config.read(filename)
    chrome_driver = config.get('Paths', 'chrome')
    interval_days = int(config.get('Scraper', 'scraper_days'))
    
    # Set Chrome option settings
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": directory,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })
    end_date = (datetime.today().strftime('%d/%m/%Y'))
    start_date = datetime.today() - timedelta(days=interval_days)
    start_date = (start_date.strftime('%d/%m/%Y'))

    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
    driver.get(
        'http://hansardpublic.parliament.sa.gov.au/#/search/0')  # Hansard website where dates is given for scraping
    time.sleep(3)
    driver.find_element_by_name('searchstart').clear()
    driver.find_element_by_name('searchstart').send_keys(start_date)  # start date for scraping
    driver.find_element_by_name('searchend').clear()
    driver.find_element_by_name('searchend').send_keys(end_date)  # end date to finish scraping
    driver.find_element_by_class_name('hansard-search-button').click()  # it checks search icon in the page after
    time.sleep(3)
    try:
        # This will select only debates from filters in the website present in left side
        driver.find_element_by_xpath((xpath)).click()
    except NoSuchElementException as exception:
        print("NO FILES TO DOWNLOAD - please increase the range of date")
        driver.quit()
        sys.exit()
    time.sleep(1)
    # Scraping all the websites that has debates and storing in the list called all_hrefs
    # Note: In this section links of individual xml page is stored
    html = driver.page_source.encode("utf-8")  # finding the current page that driver is running
    soup = BeautifulSoup(html, 'html.parser')  # taking all the html tags from the page
    all_hrefs = []  # list of all links

    # This will take the page into next page until there is next click icon
    while soup.findAll("a", title="Move to next page"):
        # looking for all <h3> tags in the page because this tag has links to the xml file of data
        for title in soup.findAll("h3"):
            hrefs = title.findAll("a", href=True)  # looking for all <a> that has href inside it
            if len(hrefs) > 0:
                hrefs = hrefs[0]["href"]
                all_hrefs.append(hrefs)  # appending all links to xml in allHrefs
        time.sleep(4)
        driver.find_element_by_id('PageLinkNext').click()  # this will click the next page icon
        time.sleep(5)
        html = driver.page_source.encode("utf-8")  # this will again grab new link to the website of another page
        soup = BeautifulSoup(html, 'html.parser')

    driver.close()
    driver.quit()

    # creating a file name to download
    downloading_filename = []
    for i in all_hrefs:
        filename = re.findall('(?<=/docid/).*$', i)
        downloading_filename.append(filename)
    downloading_filename = reduce(lambda x, y: x + y, downloading_filename)
    file_type = ".xml"
    downloading_filename = [s + file_type for s in downloading_filename]

    print("\n\nDownload file names to compare with files in directory\n\n\n", downloading_filename)
    print("\nNumber of files queued to download = ", len(downloading_filename))

    # creating a data frame to compare and drop existing files
    file_names = os.listdir(directory)  # getting file names from directory

    # this string is added later in the extracted href to complete the webpage link of individual xml file
    string = "http://hansardpublic.parliament.sa.gov.au/Pages/"
    df_all_hrefs = pd.DataFrame(all_hrefs)
    df_all_hrefs['download_file_name'] = downloading_filename
    df_all_hrefs = df_all_hrefs.drop(df_all_hrefs[df_all_hrefs.download_file_name.isin(file_names)].index.tolist())
    df_all_hrefs = [string + s for s in df_all_hrefs[0]]  # adding string to compete the webpage link

    print("\n\n\n\nLinks of XMLs ready to download \n\n\n", df_all_hrefs)
    print("\n\n\n\nTotal number of files to be downloaded after filter = ", len(df_all_hrefs))

    if len(df_all_hrefs) > 0:
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
        for i in range(len(df_all_hrefs)):
            driver.get(df_all_hrefs[i])
            driver.find_element_by_xpath(("//*[@alt=\"XML\"]")).click()  # this will download the xml file
            time.sleep(5)
        driver.close()
        driver.quit()
    else:
        print("Your directory is up to date")


# Hansard Bills calls
print("Starting Bills")
bills_directory = 'E:\\hansardbills'  # Directory of Bill files in database
bill_xpath = "//*[@title=\"Refine by: Bills\"]"  # xpath of all Bill files in Hansard website
proceeding_filter(bills_directory, bill_xpath)

# Hansard Question Time calls
print("starting Question Time")
question_time_directory = 'E:\\hansardquestiontime'  # Directory of Question Time files in database
question_time_xpath = "//*[@title=\"Refine by: Question Time\"]"  # xpath of all Question Time files in Hansard website
proceeding_filter(question_time_directory, question_time_xpath)

# Hansard Answers to Questions calls
print("starting QANDA")
answers_directory = 'E:\\hansardqna'  # Directory of Answers to Questions files in database
answers_xpath = "//*[@title=\"Refine by: Answers to Questions\"]"  # xpath of all Answers to Questions files in Hansard website
proceeding_filter(answers_directory, answers_xpath)
