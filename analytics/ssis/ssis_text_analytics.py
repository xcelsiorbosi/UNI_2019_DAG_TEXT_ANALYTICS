# This file is executed by SSIS to calculate and add to HANSARD database: word count, key words, document summary
# and whether record text matches Audit Team key terms

import pyodbc
import os
import pandas as pd
import numpy as np
from text_summary_statistics import word_count, get_keywords
from document_summary import generate_summary_from_text
from term_search import process_terms, search_key_terms


# Connect to HANSARD database
# print(pyodbc.drivers()) # Print available ODBC drivers
db_connection = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                               'Server=DA-PROD1;'
                               'Database=HANSARD;'
                               'Trusted_Connection=yes;')

db_cursor = db_connection.cursor()

# Get HANSARDFilesInfo table
info = pd.read_sql_query("SELECT ID, KeyWords, Summary, RecordText FROM HANSARD.dbo.HANSARDFilesInfo",
                         db_connection)
info = info.astype({"ID": 'str', "KeyWords": 'str', "Summary": 'str', "RecordText": 'str'})

# Get FinalText table
text = pd.read_sql_query("SELECT *  FROM HANSARD.dbo.FinalText", db_connection)
text = pd.DataFrame(text, columns=['HansardID', 'TextID', 'Text', 'WordCount'])
text = text.astype({"HansardID": 'str', "TextID": 'str', "Text": 'str', "WordCount": 'str'})

print("Starting word count ...")

def word_count_db(hansard_id, text_id, text):
    # Calculate word count for specified text and add to Final Text table
    text_word_count = 0
    if text is not None:
        text_word_count = word_count(text)

    db_cursor.execute("UPDATE HANSARD.dbo.FinalText SET WordCount = ? WHERE TextID = ? AND HansardID = ?",
                      text_word_count, text_id, hansard_id)


# Iterate through Final Text table and add word count to table if it doesn't already exist
text.loc[text['WordCount'] == 'None'].apply(
    lambda x: word_count_db(x.HansardID, x.TextID, x.Text), axis=1)  # ~66 min for 8833 records

db_connection.commit()  # Commit changes to the HANSARD database

# Get full text for each Hansard record
grouped_text = text.groupby('HansardID')['Text'].agg(lambda col: '. '.join(col))
grouped_text = pd.DataFrame(grouped_text)
grouped_text['Text'] = grouped_text.Text.replace("..", ".")
grouped_text['Text'] = grouped_text.Text.replace("!.", "!")
grouped_text['Text'] = grouped_text.Text.replace("\?.", "\?")

# Combine full text with HansardFilesInfo table
combined = pd.merge(grouped_text, info, how='inner', left_on='HansardID', right_on='ID')
combined = combined.loc[combined['KeyWords'] == 'None'] # Get rows without key words already calculated

print("Starting key words and document summaries ...")

# Iterate over Hansard records in database and add sentiment, summary and full text if they do not already exist
for index, row in combined.iterrows():
    hansard_id = row['ID']
    full_text = row['Text']

    # Calculate and add keywords to HANSARDFilesInfo table 
    key_words = get_keywords(full_text)
    db_cursor.execute("UPDATE HANSARD.dbo.HANSARDFilesInfo SET KeyWords = ? WHERE ID = ?",
                      key_words, hansard_id)

    # Document Summary
    summary = generate_summary_from_text(full_text, 3, False)
    db_cursor.execute("UPDATE HANSARD.dbo.HANSARDFilesInfo SET Summary = ? WHERE ID = ?",
                      summary, hansard_id)

    # Full Record Text
    db_cursor.execute("UPDATE HANSARD.dbo.HANSARDFilesInfo SET RecordText = ? WHERE ID = ?",
                      full_text, hansard_id)

db_connection.commit()  # Commit changes to the HANSARD database


# Determine whether text contains mentions of Audit Team Key Terms and add as new table to 
# HANSARD database. Term search is only run for Hansard ID's that do not appear in KeyTerms table. 

print("Starting key term search ...")

text_search = pd.DataFrame(text, columns=['HansardID', 'TextID', 'Text'])
text_search['TextLower'] = text_search.Text.str.lower()  # Convert to lowercase
        
#db_cursor.execute("DELETE FROM HANSARD.dbo.KeyTerms")  # Delete all rows from table
#db_connection.commit() # Commit changes to the HANSARD database
#print("Delete KeyTerms rows")

# Filter out text that have already been searched for key terms
key_terms_table = pd.read_sql_query("SELECT HansardID FROM HANSARD.dbo.KeyTerms",
                         db_connection)
key_terms_table = key_terms_table.astype({"HansardID": 'str'})
if (len(key_terms_table.index) > 0):
    hansard_records_searched = key_terms_table.HansardID.unique() # Hansard records already searched for key terms
    text_search = text_search[~text_search['HansardID'].isin(hansard_records_searched)]

# Get Excel Spreadsheet containing Audit Team key terms
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\..\\data\\AuditTeamTerms.xlsx')
excel_file = pd.ExcelFile(filename)

# Iterate through all sheets and import terms
for sheet_name in excel_file.sheet_names:
    terms = excel_file.parse(sheet_name)  # Each sheet contains the terms for a separate audit team
    terms = pd.DataFrame(terms)
    terms['Alternate'] = terms.Alternate.replace(np.nan, '', regex=True)  # Replace missing alternate terms
    terms = terms.astype({"Term": 'str', "Alternate": 'str'})
    terms['TermPattern'] = process_terms(terms.Term)  # Process term into regular expression (regex)
    terms['AlternatePattern'] = process_terms(terms.Alternate)  # Process alternate term into regex
    search_results = search_key_terms(terms, text_search, sheet_name)  # The sheet name is the name of the audit team
    
    # Add key term search results to KeyTerms table in HANSARD database
    for index, row in search_results.iterrows():
        db_cursor.execute("INSERT INTO HANSARD.dbo.KeyTerms([HansardID],[TextID],[Term],[AuditTeam]) VALUES (?,?,?,?)",
                          row['HansardID'],
                          row['TextID'],
                          row['Term'],
                          row['AuditTeam'])
    
    print("Committed Terms for Audit Team:", sheet_name, search_results.shape, sep=" ")

db_connection.commit() # Commit changes to the HANSARD database

# Close connection to the database
db_cursor.close()
db_connection.close()
