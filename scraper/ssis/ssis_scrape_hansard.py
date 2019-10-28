# Import library
import configparser
from hansard_scraper import scrape_hansard

# Read required values from projects configuration file
config = configparser.ConfigParser()
config.read('..\\config.ini')
bill_directory = config['Paths']['bills']
answers_directory = config['Paths']['answers']
question_time_directory = config['Paths']['answers']

# Scrape Hansard Records
scrape_hansard(bill_directory, "//*[@title=\"Refine by: Bills\"]")  # Scrape Bills records
scrape_hansard(answers_directory,
               "//*[@title=\"Refine by: Answers to Questions\"]")  # Scrape Answers to Questions records
scrape_hansard(question_time_directory, "//*[@title=\"Refine by: Question Time\"]")  # Scrape Question Time records
