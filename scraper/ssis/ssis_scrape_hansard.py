# Import library
import configparser
import os
from hansard_scraper import scrape_hansard

# Read required values from projects configuration file
config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\..\\config.ini')
config.read(filename)
bill_directory = config['Paths']['bills']
answers_directory = config['Paths']['answers']
question_time_directory = config['Paths']['question_time']

# Scrape Hansard Records
scrape_hansard(bill_directory, "//*[@title=\"Refine by: Bills\"]")  # Scrape Bills records
scrape_hansard(answers_directory,
               "//*[@title=\"Refine by: Answers to Questions\"]")  # Scrape Answers to Questions records
scrape_hansard(question_time_directory, "//*[@title=\"Refine by: Question Time\"]")  # Scrape Question Time records
