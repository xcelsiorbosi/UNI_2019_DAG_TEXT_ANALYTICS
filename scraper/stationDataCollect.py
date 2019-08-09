import selenium
import pandas as pd 
import sys, os
import time
# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options
from selenium import webdriver
# driver = webdriver.Firefox()

from selenium.webdriver.support.ui import Select


cwd = os.getcwd()
# just print this to see where it is
# BASE_DIR = os.path.join( os.path.dirname( __file__ ),'' )
# print (BASE_DIR, 'this is base')


#this is the setup for silenium
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": cwd,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})



def getData(address):
	driver = webdriver.Chrome(chrome_options=options)
	driver.set_page_load_timeout(10)
	#load page
	driver.get(address)
	#figure out where to put the refresh
	# driver.refresh()

	#wait for page to load before proceeding
	# driver.maximize_window()
	driver.implicitly_wait(4)
	#click the link for the download
	# driver.find_element_by_class_name("Data file for daily rainfall data for all years").click()
	# driver.find_element_by_id("Data file for daily rainfall data for all years").click()
	# driver.find_element_by_id("All years of data").click()
	# elem = browser.find_element_by_link_text("All years of data")

	driver.find_element_by_xpath(u'//a[text()="All years of data"]').click()



	# change this to a method that waits for download to complete
	time.sleep(1)
	print('waited 1')
	time.sleep(1)
	print('waited 1')
	time.sleep(1)
	print('waited 1')
	time.sleep(1)
	print('waited 1')
	time.sleep(1)
	print('waited 1')
	time.sleep(1)
	print('waited 1')

	# driver.find_element_by_link_text("All years of data").click()
	# driver.find_element_by_xpath('//*[@title="All years of data"]').click()

	# find_element_by_link_text

	print ('--------------------------------------------------------------------')

	driver.quit()

# print (address)
# getData(address)

# link = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num='+station


# stations = ['23097','23090','23057','23037','23031','23000','23034','23046','22029','16065','17099','23703','24025','24002','21008','25050','22823','22801','22802','26095','26044','26005','22803','18012','21131','21014','18014','18116','18230','16007','16090','18110','26045','26091','18191','18229','18217','23083','22046','18069','16013','16097','24511','18030','21020','20028','23849','19017','23894','22006','22050','23307','25006','25507','25557','18040','22807','22841','25554','26070','23818','23887','18044','26013','16081','25509','25562','17005','17110','23801','25034','24023','24024','26016','22008','18114','16085','17031','17126','23872','24518','22031','18052','18195','17096','17123','23733','26019','23878','23763','17070','26021','16067','23842','24521','24584','23738','26023','26099','18115','23885','16032','18192','18106','23321','23373','17114','17043','26089','26100','23013','23875','22816','22843','22814','23015','26036','23883','18139','18201','16092','19036','19066','18070','18181','21118','21139','21043','22015','24016','24048','26026','26105','23343','23020','23122','16096','16089','23816','21046','21133','22049','23745','23785','23747','24580','18079','26082','24536','16044','16098','22030','23804','23751','23103','23092','24018','24045','24041','24033','22018','18103','18120','19053','16001','18083','19062','20026','20062']

stations = ['023752']
print (stations)

dropList = []

# split this function out from rain, temp and wind
# need to send in parameters and other instructions specific to the landing pages
# also add different store directories for the different data sets
def makeAddress(stations):
	for station in stations:
		addressRainfall = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num='+station
		
		addressTemp ='http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num='+station
		addressWind = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=201&p_display_type=dwo&p_startYear=&p_c=&p_stn_num=' + station

		print (addressRainfall)
		print (addressTemp)
		try:
			getData(addressRainfall)
			getData(addressTemp)
		except:
			dropList.append(station)
			continue
makeAddress(stations)
print (dropList)

df = pd.DataFrame(data = dropList,columns=['station'])
print (df)
stationID = 1
df.to_csv('Data/'+'drop.csv')


