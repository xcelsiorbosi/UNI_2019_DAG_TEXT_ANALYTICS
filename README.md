# Hansard Data Mining Project

The Hansard Data Mining Project is a University project (Semester 2 2019) being completed at the University of South Australia with the [Auditor-General's Department](https://www.audit.sa.gov.au/) (AGD). The objective of this project is to develop a proof-of-concept dashboard for AGD to analyse unstructured text data sources, focusing on Hansard records from South Australian Parliament. [Hansard](http://hansardpublic.parliament.sa.gov.au/#/search/0) is the complete record of Parliamentary debates and questions. The dashboard would allow AGD staff to better interrogate and summarise discussions in Hansard to identify relevant information for audits. It would ingest Hansard extracts from Parliament's website and provide a dashboard for auditors to review

This project contains Python code to scrape the data from [Hansard](http://hansardpublic.parliament.sa.gov.au/#/search/0), process this data, and store the data in SQL Server. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites 
Listed below are what is required to run this project. 

* [Python](https://www.python.org/downloads/) 
    * Minimum version Python 3.7
* [R](https://www.r-project.org/)
    * Minimum version R 3.6.1
* [Selenium](https://selenium-python.readthedocs.io/installation.html)
    * Python module selenium can be installed using pip: ``` $pip install selenium  ```
* [Chrome Web Driver](https://chromedriver.chromium.org/getting-started)
* [Google Chrome](https://www.google.com/chrome/)
* [Saxon: XSLT and XQuery Processor](http://saxon.sourceforge.net/)
    * Version 9 provided in xslt/saxon directory

Additional prerequisites, such as Python and R libraries, are described in the Installation and Deployment Guide in the documentation directory. 

### Installation and Deployment

An Installation and Deployment Guide for this project is included in the documentation directory.

## Contributing
When contributing to this project follow these steps:
1.	Fork the project & clone locally
2.	Create an upstream remote and sync your local copy before you branch
3.	Branch for each separate piece of work. Give the branch a descriptive name in lowercase with hypens to separate words e.g. xml-transformation-logic.
4.	Do the work and write good commit messages
5.	Push to your origin repository
6.	Create a new Pull Request in GitHub and assign at least one project team member to review

Full detailed instructions on how to complete each of these steps see [The beginner's guide to contributing to a GitHub project](https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/)

### Naming Conventions
Project code should follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python to maintain readability. 

There is a command-line program, [pycodestyle](https://github.com/PyCQA/pycodestyle), that can check your code for conformance. Install it by running the following command in your terminal:

``` $ pip install pycodestyle ```

Then run it on a file or series of files to get a report of any violations.

``` $ pycodestyle optparse.py ```

The table below outlines some of the common naming styles in Python code and when you should use them:

|Type	|Naming Convention	|Examples|
|---|---|---|
|Function	|Use a lowercase word or words. Separate words by underscores to improve readability.	|function, my_function|
|Variable	|Use a lowercase single letter, word, or words. Separate words with underscores to improve readability.	|x, var, my_variable|
|Class	|Start each word with a capital letter. Do not separate words with underscores. This style is called camel case.	|Model, MyClass|
|Method	|Use a lowercase word or words. Separate words with underscores to improve readability.	|class_method, method|
|Constant	|Use an uppercase single letter, word, or words. Separate words with underscores to improve readability.	|CONSTANT, MY_CONSTANT, MY_LONG_CONSTANT|
|Module	|Use a short, lowercase word or words. Separate words with underscores to improve readability.	|module.py, my_module.py|
|Package	|Use a short, lowercase word or words. Separate words with underscores if it improves readability.| package, package_input|

Additional reading resources on using PEP 8 style guide:
* [Python Naming Conventions](https://visualgit.readthedocs.io/en/latest/pages/naming_convention.html)
* [Pep 8: Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

## Authors
* Aaron Butler - *Text analytics*
* Bipin Karki - *Data Scraper and text analytics*
* Katherine Noack - *Dashboards and text analytics*
* Mahmoud Yousefi - *ETL and text analytics*

## Acknowledgments
* Eric Lam - *University Mentor*
* James Baker at AGD - *Project Owner*
* Aaron Steicke at AGD - *Project Owner*
* Andrew Corrigan at AGD - *Project Sponsor*
* Project Reference group at AGD
* University of South Australia
* [README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) by [PurpleBooth](https://github.com/PurpleBooth)