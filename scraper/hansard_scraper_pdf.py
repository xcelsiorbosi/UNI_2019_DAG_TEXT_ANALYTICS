# Import all necessary packages for the project.
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re, datetime

cwd = os.getcwd()
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": cwd,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(chrome_options=options)  # need to download chromedriver.exe and give path

driver.get('http://hansardpublic.parliament.sa.gov.au/#/search/0')  # Hansard website
time.sleep(3)
driver.find_element_by_name('searchstart').clear()
driver.find_element_by_name('searchstart').send_keys("12/02/2019")  # start date for scraping
driver.find_element_by_name('searchend').clear()
driver.find_element_by_name('searchend').send_keys("15/02/2019")  # end date to finish scraping
driver.find_element_by_class_name('hansard-search-button').click()
time.sleep(3)
driver.find_element_by_xpath(
    "//*[@title=\"Refine by: Answers to Questions\"]").click()  # this will select only debates
time.sleep(3)

# Scraping all the websites that has debates and storing in the list called allherfs

html = driver.page_source.encode("utf-8")  # getting current url
# print (driver.current_url)
soup = BeautifulSoup(html, 'html.parser')  # getting all html tags of current url into soup variable
string = "http://hansardpublic.parliament.sa.gov.au/Pages/"  # later adding this into
# iteration = 1     # Checking the loop status
all_hrefs = []  # creating empty list to add links of individual pdf later
dictionary = {}  # creating empty dictionary
while soup.findAll("a", title="Move to next page"):  # this will take driver to next page after completing scrping the current page
    #     print("Iteration:", iteration)
    for tag in soup.findAll("h3"):  # <h3> is a tag where individual debates links are present
        hrefs = tag.findAll("a", href=True)  # all <a> tags inside h3 has all individual debates links
        if len(hrefs) > 0:
            head = tag.getText("a", "title")  # getting title of all topics
            head = head.split("-")[-1]
            date = re.search('\d{1,2}/\d{1,2}/\d{4}', head)  # shere dates are extracted from the headline
            dates = datetime.datetime.strptime(date.group(), '%d/%m/%Y').date()  # converting date into datetime format
            # print(date)
            hrefs = hrefs[0]["href"]  # importing links into hrefs
            # print(hrefs)
            dictionary[dates] = hrefs  # since same dates has same pdf we are only taking links of unique dates
            # allHrefs.append(hrefs)
    # print(dictionary)
    time.sleep(4)
    driver.find_element_by_id('PageLinkNext').click()  # clicks next page
    time.sleep(4)
    html = driver.page_source.encode("utf-8")  # getting new page source
    soup = BeautifulSoup(html, 'html.parser')  # getting all html from the page
    # iteration = iteration + 1

driver.close()
print(dictionary)
all_hrefs = dictionary.values()  # allHrefs has links to all pdf file
all_hrefs = [string + s for s in all_hrefs]

# Scrapping all pdf files for all parliament sittings
# Single pdf contains all the debates on that specific date whereas single xml has only one debate
for i in range(len(all_hrefs)):
    driver = webdriver.Chrome(executable_path='C:\\Users\\Bipin Karki\\Desktop\\chromedriver.exe',
                              chrome_options=options)
    driver.get(all_hrefs[i])
    driver.find_element_by_xpath("//*[@title=\"Download Daily PDF\"]").click()  # downloading individual pdf
    time.sleep(4)
    driver.close()
