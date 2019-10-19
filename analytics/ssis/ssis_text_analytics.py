import pyodbc
import os
import pandas as pd
from text_summary_statistics import word_count, get_keywords
from document_summary import smart_truncate, generate_summary_from_text

# Connect to HANSARD database
db_connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=DA-PROD1;'
                      'Database=HANSARD;'
                      'Trusted_Connection=yes;')
 
db_cursor = db_connection.cursor()

# Get HANSARDFilesInfo table
info = pd.read_sql_query("SELECT ID, KeyWords, Summary, TruncatedSummary FROM HANSARD.dbo.HANSARDFilesInfo", 
                         db_connection)
info = info.astype({"ID":'str', "KeyWords":'str', "Summary":'str', "TruncatedSummary":'str'}) 

# Get FinalText table
text = pd.read_sql_query("SELECT *  FROM HANSARD.dbo.FinalText", db_connection)
text = pd.DataFrame(text, columns= ['HansardID','TextID','Text','WordCount'])
text = text.astype({"HansardID":'str', "TextID":'str', "Text":'str', "WordCount":'int'}) 

def word_count_db(hansard_id, text_id, text):
    # Calculate word count for specified text and add to Final Text table
    text_word_count = 0
    if text is not None:
        text_word_count = word_count(text)
    
    print(hansard_id, text_id, text_word_count, sep=" -- ") # DELETE WHEN FINISH TESTING
    db_cursor.execute("UPDATE HANSARD.dbo.FinalText SET WordCount = ? WHERE TextID = ? AND HansardID = ?", 
                      text_word_count, text_id, hansard_id)

# Iterate through Final Text table and add word count to table if it doesn't already exist
text.loc[text['WordCount'] == None].apply(
    lambda x:  word_count_db(x.HansardID, x.TextID, x.Text), axis=1) # 4019.269sec ~66 min

# Get full text for each Hansard record
grouped_text = text.groupby('HansardID')['Text'].agg(lambda col: '. '.join(col))
grouped_text = pd.DataFrame(grouped_text)
grouped_text['Text'] = grouped_text.Text.replace("..",".")
grouped_text['Text'] = grouped_text.Text.replace("!.","!")
grouped_text['Text'] = grouped_text.Text.replace("\?.","\?")

# Combine full text with HansardFilesInfo table
combined = pd.merge(grouped_text, info, how='inner', left_on = 'HansardID', right_on = 'ID')

# Iterate over all Hansard records in database and add sentiment and summaries if they do not already exist
for index, row in combined.iterrows():    
    hansard_id = row['ID']
    full_text = row['Text']

    # Calculate and add keywords to HANSARDFilesInfo table if it does not exist
    if row['KeyWords'] == 'None':
        key_words = get_keywords(full_text)
        print(hansard_id, key_words, sep=" -- ") # DELETE WHEN FINISH TESTING
        db_cursor.execute("UPDATE HANSARD.dbo.HANSARDFilesInfo SET KeyWords = ? WHERE ID = ?", 
                          key_words, hansard_id)

    # Document Summaries
    if row['Summary'] == 'None':
        summary = generate_summary_from_text(full_text, 3, False)
        print(hansard_id, summary, sep=" -- ") # DELETE WHEN FINISH TESTING
        db_cursor.execute("UPDATE HANSARD.dbo.HANSARDFilesInfo SET Summary = ? WHERE ID = ?", 
                          summary, hansard_id)

    if row['TruncatedSummary'] == 'None':
        summary = smart_truncate(full_text)
        print(hansard_id, summary, sep=" -- ") # DELETE WHEN FINISH TESTING
        db_cursor.execute("UPDATE HANSARD.dbo.HANSARDFilesInfo SET TruncatedSummary = ? WHERE ID = ?", 
                          summary, hansard_id)

# Determine whether text contains mentions of Audit Team Key Terms and add as new table to 
# HANSARD database. Everytime this term search is run will replace the table in the database in case
# of changes to key terms listed in the spreadsheet. 

text_search = pd.DataFrame(text, columns= ['HansardID','TextID','Text'])
text_search['Text'] = text_search.Text.str.lower() # Convert to lowercase

# Get Audit teams search terms
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '..\\..\\data\\AuditTeamTerms.xlsx')

data = pd.read_excel(filename, sheet_name="Performance Audit")
performance = pd.DataFrame(data)
performance['ProcessedTerm'] = performance.Term.str.lower() # Convert to lowercase

data = pd.read_excel(filename, sheet_name="Local Government Audit")
government = pd.DataFrame(data)
government['ProcessedTerm'] = government.Term.str.lower() # Convert to lowercase

data = pd.read_excel(filename, sheet_name="IT Audit")
it = pd.DataFrame(data)
it['ProcessedTerm'] = it.Term.str.lower() # Convert to lowercase

# Performance Audit Team Terms
pattern = '|'.join(r"{}".format(x) for x in performance.ProcessedTerm)
text_search['MatchedTerm'] = text_search.Text.str.extract('(' + pattern + ')', expand=False)
performance_terms = pd.merge(performance, text_search, left_on= 'ProcessedTerm', right_on='MatchedTerm').drop('MatchedTerm', axis=1)
performance_terms.columns = ['Term','ProcessedTerm','HansardID','TextID','Text']
del text_search['MatchedTerm'] # Delete newly added column from text data
del performance_terms['Text'] # Delete unneeded Text column from results
del performance_terms['ProcessedTerm'] # Delete unneeded ProcessedTerm column from results
performance_terms['AuditTeam'] = "Performance"

# Local Government Audit Team Terms
pattern = '|'.join(r"{}".format(x) for x in government.ProcessedTerm)
text_search['MatchedTerm'] = text_search.Text.str.extract('('+ pattern + ')', expand=False)
government_terms = pd.merge(government, text_search, left_on= 'ProcessedTerm', right_on='MatchedTerm').drop('MatchedTerm', axis=1)
government_terms.columns = ['Term','Alternate','ProcessedTerm','HansardID','TextID','Text']
del text_search['MatchedTerm'] # Delete newly added column from text data
del government_terms['Text'] # Delete unneeded Text column from results
del government_terms['Alternate'] # Delete unneeded Alternate column from results
del government_terms['ProcessedTerm'] # Delete unneeded ProcessedTerm column from results
government_terms['AuditTeam'] = "Local Government"

# IT Audit Team Terms
pattern = '|'.join(r"{}".format(x) for x in it.ProcessedTerm)
text_search['MatchedTerm'] = text_search.Text.str.extract('('+ pattern + ')', expand=False)
it_terms = pd.merge(it, text_search, left_on= 'ProcessedTerm', right_on='MatchedTerm').drop('MatchedTerm', axis=1)
it_terms.columns = ['Term','ProcessedTerm','HansardID','TextID','Text']
del text_search['MatchedTerm'] # Delete newly added column from text data
del it_terms['Text'] # Delete unneeded Text column from results
del it_terms['ProcessedTerm'] # Delete unneeded ProcessedTerm column from results
it_terms['AuditTeam'] = "IT"

# Merge search results
merged_data = pd.concat([performance_terms, government_terms,it_terms], ignore_index=True)
merged_data = merged_data.drop_duplicates() # Drop duplicate rows
print(merged_data.shape)

# Add key term search results to KeyTerms table in HANSARD database
db_cursor.execute("DELETE FROM HANSARD.dbo.KeyTerms") # Delete all rows from table
for index,row in merged_data.iterrows():
    db_cursor.execute("INSERT INTO HANSARD.dbo.KeyTerms([HansardID],[TextID],[Term],[AuditTeam]) VALUES (?,?,?,?)", 
                   row['HansardID'], 
                   row['TextID'], 
                   row['Term'],
                   row['AuditTeam']) 

# Commit changes to the HANSARD database
db_connection.commit() 

# Close connection to the database
db_cursor.close()
db_connection.close()
