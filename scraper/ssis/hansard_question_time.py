# Import library
from datetime import datetime
from datetime import timedelta
import configparser
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

# Read required values from projects configuration file
config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\..\\config.ini')
config.read(filename)
chrome_driver = config['Paths']['chrome']
interval_days = int(config['Scraper']['scraper_days'])
question_time_directory = config['Paths']['question_time']

# Set start date and end date
end_date = (datetime.today().strftime('%d/%m/%Y'))
start_date = datetime.today() - timedelta(days=interval_days)
start_date = (start_date.strftime('%d/%m/%Y'))

options = webdriver.ChromeOptions()  # option settings
options.add_experimental_option("prefs", {
    "download.default_directory": question_time_directory,  # path of folder where xmls needs to be saved
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)

driver.get('http://hansardpublic.parliament.sa.gov.au/#/search/0')  # hansard website where dates is given for scraping
time.sleep(3)
driver.find_element_by_name('searchstart').clear()
driver.find_element_by_name('searchstart').send_keys(start_date)  # start date for scraping
driver.find_element_by_name('searchend').clear()
driver.find_element_by_name('searchend').send_keys(end_date)  # end date to finish scraping
driver.find_element_by_class_name(
    'hansard-search-button').click()  # it clicks search icon in the page after dates are specified
time.sleep(3)
driver.find_element_by_xpath("//*[@title=\"Refine by: Question Time\"]").click()  # this will select only question time from filters in the website
time.sleep(3)

# Scraping all the websites that has debates and storing in the list called allherfs
# note: In this section links of individual xml page is stored
html = driver.page_source.encode("utf-8")  # finding the current page that driver is running
# print (driver.current_url)
soup = BeautifulSoup(html, 'html.parser')  # taking all the html tags from the page
string = "http://hansardpublic.parliament.sa.gov.au/Pages/"  # this string is added later in the extracted href to complete the webpage link of individual xml file
# iteration = 1     Checking the loop status
allHrefs = []  # list of all links
while soup.findAll("a",
                   title="Move to next page"):  # this will take the page into next page until there is next click icon
    #     print("Iteration:", iteration)
    for title in soup.findAll(
            "h3"):  # looking for all <h3> tags in the page because this tag has links to the xml file of data
        hrefs = title.findAll("a", href=True)  # looking for all <a> that has href inside it
        if len(hrefs) > 0:
            hrefs = hrefs[0]["href"]
            allHrefs.append(hrefs)  # appending all links to xml in allHrefs
    time.sleep(4)
    driver.find_element_by_id('PageLinkNext').click()  # this will click the next page icon
    time.sleep(10)
    html = driver.page_source.encode("utf-8")  # this will again grab new link to the website of another page
    soup = BeautifulSoup(html, 'html.parser')
#     iteration = iteration + 1
allHrefs = [string + s for s in allHrefs]  # adding string to compete the webpage link
driver.close()
# allHrefs contains links of individual xml file page


# Scraping all XML files for individual debates
for i in range(len(allHrefs)):
    driver = webdriver.Chrome(
        executable_path=chrome_driver,
        chrome_options=options)
    driver.get(allHrefs[i])
    driver.find_element_by_xpath(("//*[@alt=\"XML\"]")).click()  # this will download the xml file
    time.sleep(10)
    driver.close()
