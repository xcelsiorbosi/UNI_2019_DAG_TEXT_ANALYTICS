import pyodbc
import pandas as pd
import time
from text_summary_statistics import word_count, get_keywords
from document_summary import smart_truncate, generate_summary

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
    
    print(hansard_id, text_id, text_word_count, sep=" -- ")
    db_cursor.execute("UPDATE HANSARD.dbo.FinalText SET WordCount = ? WHERE TextID = ? AND HansardID = ?", 
                      text_word_count, text_id, hansard_id)

t0 = time.time()

# Iterate through Final Text table and add word count to table if it doesn't already exist
text.loc[text['WordCount'] == None].apply(
    lambda x:  word_count_db(x.HansardID, x.TextID, x.Text), axis=1)

t1 = time.time()
total_time = t1-t0
print("Time =", total_time) # 4019.269sec ~66 min

# Iterate through Final Text table and add word count to table if it doesn't already exist
#for row in db_cursor:
#for index, row in text.iterrows():
#    text = row['Text']
#    text_word_count = row['WordCount']

#    if text_word_count is not None:
#        print("Already exists!")
#        continue
#    
#    text_word_count = 0
#    if text is not None:
#        text_word_count = word_count(text)
#    
#    #db_cursor.execute("INSERT into HANSARD.dbo.FinalText(WordCount) VALUES (?)", text_words)
#    hansard_id = row['HansardID']
#    text_id = row['TextID']    
#    print(hansard_id, text_id, text_word_count, sep=" - ")
#    db_cursor.execute("UPDATE HANSARD.dbo.FinalText SET WordCount = ? WHERE TextID = ? AND HansardID = ?", 
#                      text_word_count, text_id, hansard_id)
    
# Get full text for each Hansard record
grouped_text = text.groupby('HansardID')['Text'].agg(lambda col: '. '.join(col))
grouped_text = pd.DataFrame(grouped_text)
#grouped_text['HansardID'] = grouped_text.index
grouped_text['Text'] = grouped_text.Text.replace("..",".")
grouped_text['Text'] = grouped_text.Text.replace("!.","!")
grouped_text['Text'] = grouped_text.Text.replace("\?.","\?")
#grouped_text.reset_index() # Reset index and add HansardID as column
#grouped_text.reset_index(drop=True)
#grouped_text = grouped_text.astype({"Text":'str', "HansardID":'int'}) 

combined = pd.merge(grouped_text, info, how='inner', left_on = 'HansardID', right_on = 'ID')

for index, row in combined.iterrows():    
    hansard_id = row['ID']
    full_text = row['Text']

    # Calculate and add keywords to HANSARDFilesInfo table if it does not exist
    if row['KeyWords'] == 'None':
        key_words = get_keywords(full_text)
        print(hansard_id, key_words, sep=" -- ")
        db_cursor.execute("UPDATE HANSARD.dbo.HANSARDFilesInfo SET KeyWords = ? WHERE ID = ?", 
                          key_words, hansard_id)

    # TODO: Document Summaries

    # TODO: Audit Team Key Terms

db_connection.commit()

