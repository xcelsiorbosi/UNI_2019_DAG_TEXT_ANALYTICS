# Import libraries
import configparser
import time
import os
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium import webdriver


def scrape_hansard(output_directory, debate_filter):

    # Read required values from projects configuration file
    config = configparser.ConfigParser()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '..\\..\\config.ini')
    config.read(filename)
    chrome_driver = config['Paths']['chrome']
    interval_days = int(config['Scraper']['scraper_days'])
    
    # Set start date and end date
    end_date = (datetime.today().strftime('%d/%m/%Y'))
    start_date = datetime.today() - timedelta(days=interval_days)
    start_date = (start_date.strftime('%d/%m/%Y'))

    options = webdriver.ChromeOptions()  # option settings
    options.add_experimental_option("prefs", {
        "download.default_directory": output_directory,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)

    # Hansard website where dates is given for scraping
    driver.get('http://hansardpublic.parliament.sa.gov.au/#/search/0')
    time.sleep(3)
    driver.find_element_by_name('searchstart').clear()
    driver.find_element_by_name('searchstart').send_keys(start_date)  # start date for scraping
    driver.find_element_by_name('searchend').clear()
    driver.find_element_by_name('searchend').send_keys(end_date)  # end date to finish scraping
    driver.find_element_by_class_name('hansard-search-button').click()  # it clicks search icon in the page after
    time.sleep(3)
    driver.find_element_by_xpath(debate_filter).click()  # select only debates from filters in the website present in left side
    time.sleep(3)

    # Scraping all the websites that has debates and storing in the list called all_hrefs
    # Note: In this section the links of individual XML pages are stored
    html = driver.page_source.encode("utf-8")  # Find the current page that driver is running
    soup = BeautifulSoup(html, 'html.parser')  # Take all the HTML tags from the page
    string = "http://hansardpublic.parliament.sa.gov.au/Pages/"  # this string is added later in the extracted href to complete the webpage link of individual XML file
    all_hrefs = []  # all_hrefs contains links of individual XML file page
    while soup.findAll("a", title="Move to next page"):  # Take the page into next page until there is next click icon
        for title in soup.findAll("h3"):  # Look for <h3> tags in the page because this tag has links to the XML file
            hrefs = title.findAll("a", href=True)  # looking for all <a> that has href inside it
            if len(hrefs) > 0:
                hrefs = hrefs[0]["href"]
                all_hrefs.append(hrefs)  # appending all links to XML in all_hrefs
        time.sleep(4)
        driver.find_element_by_id('PageLinkNext').click()  # this will click the next page icon
        time.sleep(10)
        html = driver.page_source.encode("utf-8")  # this will again grab new link to the website of another page
        soup = BeautifulSoup(html, 'html.parser')
    
    all_hrefs = [string + s for s in all_hrefs]  # adding string to compete the webpage link

    # Scrape all XML files for individual debates
    for i in range(len(all_hrefs)):        
        driver.get(all_hrefs[i])
        driver.find_element_by_xpath("//*[@alt=\"XML\"]").click()  # download the XML file
        #time.sleep(10)
    
    time.sleep(10)
    
    driver.close()
    driver.quit()
