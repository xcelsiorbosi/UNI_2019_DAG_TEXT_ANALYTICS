import pandas as pd

data = pd.read_excel ("..\\data\\Hansard1102019.xlsx", sheet_name="Text")
text = pd.DataFrame(data, columns= ['HansardID','TextID','Text'])
text = text.astype({"HansardID":'str', "TextID":'str', "Text":'str'})
text.Text = text.Text.str.lower() # Convert to lowercase

data = pd.read_excel("..\\data\\AuditTeamTerms.xlsx", sheet_name="Performance Audit")
performance = pd.DataFrame(data)
performance['ProcessedTerm'] = performance.Term.str.lower() # Convert to lowercase

data = pd.read_excel("..\\data\\AuditTeamTerms.xlsx", sheet_name="Local Government Audit")
government = pd.DataFrame(data)
government['ProcessedTerm'] = government.Term.str.lower() # Convert to lowercase

data = pd.read_excel("..\\data\\AuditTeamTerms.xlsx", sheet_name="IT Audit")
it = pd.DataFrame(data)
it['ProcessedTerm'] = it.Term.str.lower() # Convert to lowercase

# Performance Audit Team Terms
pattern = '|'.join(r"{}".format(x) for x in performance.ProcessedTerm)
text['MatchedTerm'] = text.Text.str.extract('(' + pattern + ')', expand=False)
performance_terms = pd.merge(performance, text, left_on= 'ProcessedTerm', right_on='MatchedTerm').drop('MatchedTerm', axis=1)
performance_terms.columns = ['Term','ProcessedTerm','FileName','TextID','Text']
del text['MatchedTerm'] # Delete newly added column from text data
del performance_terms['Text'] # Delete unneeded Text column from results
del performance_terms['ProcessedTerm'] # Delete unneeded ProcessedTerm column from results
performance_terms['AuditTeam'] = "Performance"

# Local Government Audit Team Terms
pattern = '|'.join(r"{}".format(x) for x in government.ProcessedTerm)
text['MatchedTerm'] = text.Text.str.extract('('+ pattern + ')', expand=False)
government_terms = pd.merge(government, text, left_on= 'ProcessedTerm', right_on='MatchedTerm').drop('MatchedTerm', axis=1)
government_terms.columns = ['Term','Alternate','ProcessedTerm','FileName','TextID','Text']
del text['MatchedTerm'] # Delete newly added column from text data
del government_terms['Text'] # Delete unneeded Text column from results
del government_terms['Alternate'] # Delete unneeded Alternate column from results
del government_terms['ProcessedTerm'] # Delete unneeded ProcessedTerm column from results
government_terms['AuditTeam'] = "Local Government"

pattern = '|'.join(r"{}".format(x) for x in it.ProcessedTerm)
text['MatchedTerm'] = text.Text.str.extract('('+ pattern + ')', expand=False)
it_terms = pd.merge(it, text, left_on= 'ProcessedTerm', right_on='MatchedTerm').drop('MatchedTerm', axis=1)
it_terms.columns = ['Term','ProcessedTerm','FileName','TextID','Text']
del text['MatchedTerm'] # Delete newly added column from text data
del it_terms['Text'] # Delete unneeded Text column from results
del it_terms['ProcessedTerm'] # Delete unneeded ProcessedTerm column from results
it_terms['AuditTeam'] = "IT"

# Merge results and output to Excel
merged_data = pd.concat([performance_terms, government_terms,it_terms], ignore_index=True)
merged_data = merged_data.drop_duplicates() # Drop duplicate rows
merged_data.to_excel('.\\TermSearch.xlsx', sheet_name='TermSearch', index=False)


