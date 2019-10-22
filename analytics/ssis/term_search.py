import pandas as pd
import numpy as np
import time


def process_term(term):
    if "?=.*" in term:
        # Search for terms separated by any text and in any order
        term = r'(?=.*\b' + term + r'\b)'
    elif not term:
        # Term does not exist and should not be processed further
        return ""
    else:
        # Search for term as a whole word
        term = r'\b(' + term + ')' + r'\b'  # \b word boundary

    return term


def process_terms(terms):
    processed = terms.str.lower()  # Convert to lowercase
    processed = processed.str.strip()  # Trim any whitespace from ends

    # Search for terms separated by '+' in any order: Use regex (?=.*\bTerm\b)(?=.*\bTerm\b) where \b is a word boundary
    processed = processed.str.replace(' *\+ *', r'\\b)(?=.*\\b')
    processed = processed.apply(lambda x: process_term(x))

    return processed


# Search for Key Terms in Hansard Text
def search_key_terms(terms_df, text_df, audit_team_name):
    results = pd.DataFrame().reindex_like(text_df)
    results['Term'] = np.NaN
    del results['Text']  # Delete unneeded Text column from results
    del results['TextLower']  # Delete unneeded Text column from results
    results = results.dropna()  # Delete all rows

    for index, row in terms_df.iterrows():
        # Search for match to term
        match_term = text_df.TextLower.str.contains(row['TermPattern'], case=False, regex=True) | \
                     text_df.Text.str.contains(row['TermPattern'], case=False, regex=True)

        match = pd.DataFrame(match_term, columns=['Term'])

        # Search for match to alternate term
        if row['AlternatePattern']:
            # Match to alternate term is true if a match has already been found for the original term
            match_alternate = text_df.TextLower.str.contains(row['AlternatePattern'], case=False, regex=True) | \
                              text_df.Text.str.contains(row['AlternatePattern'], case=False, regex=True)
            match_alternate = pd.DataFrame(match_alternate, columns=['Alternate'])
            match['Term'] = match['Term'] | match_alternate['Alternate']

        if not match.empty:
            match = pd.concat([text_df.reset_index(drop=True), match], axis=1)
            del match['Text']  # Delete unneeded Text column from results
            del match['TextLower']  # Delete unneeded TextLower column from results
            match = match.loc[match.Term, :]  # drop rows that did not match term
            match['Term'] = row['Term']
            results = pd.concat([results, match], ignore_index=True, sort=False)  # Add matched terms to final result

    results = results.drop_duplicates()  # Drop duplicate rows
    results['AuditTeam'] = audit_team_name
    return results


def import_spreadsheet_terms(path, sheet_name):
    excel_data = pd.read_excel(path, sheet_name=sheet_name)
    excel_data = pd.DataFrame(excel_data)
    excel_data['Alternate'] = excel_data.Alternate.replace(np.nan, '', regex=True)  # Replace missing alternate terms
    excel_data = excel_data.astype({"Term": 'str', "Alternate": 'str'})
    excel_data['TermPattern'] = process_terms(excel_data.Term)  # Process term into regular expression (regex)
    excel_data['AlternatePattern'] = process_terms(excel_data.Alternate)  # Process alternate term into regex
    return excel_data


# Import data from spreadsheet
text = pd.read_excel("..\\data\\Hansard1102019.xlsx", sheet_name="Text")
text = pd.DataFrame(text, columns=['HansardID', 'TextID', 'Text'])
text = text.astype({"HansardID": 'str', "TextID": 'str', "Text": 'str'})
text['TextLower'] = text.Text.str.lower()  # Convert to lowercase

# Import key terms from spreadsheet
performance = import_spreadsheet_terms("..\\data\\AuditTeamTerms.xlsx", "Performance")
government = import_spreadsheet_terms("..\\data\\AuditTeamTerms.xlsx", "Local Government")
it = import_spreadsheet_terms("..\\data\\AuditTeamTerms.xlsx", "IT")

# TODO: Iterate through all sheets and import terms
#df = pd.read_excel('excel_file_path.xls')
#excel_file = pd.ExcelFile('excel_file_path.xls') # this will read the first sheet into df
#for sheet_name in excel_file.sheet_names:
#    terms = excel_file.parse(sheet_name) # Each sheet contains the terms for a separate audit team
#    terms = pd.DataFrame(terms)
#    terms['Alternate'] = terms.Alternate.replace(np.nan, '', regex=True)  # Replace missing alternate terms
#    terms = terms.astype({"Term": 'str', "Alternate": 'str'})
#    terms['TermPattern'] = process_terms(terms.Term)  # Process term into regular expression (regex)
#    terms['AlternatePattern'] = process_terms(terms.Alternate)  # Process alternate term into regex
#    search_results = search_key_term(terms, text, sheet_name) # The sheet name is the name of the audit team

# TODO: Only run for HansardID's not already found in KeyTerms table.
# TODO: If want to trigger a complete rebuild of the table because the clients spreadsheet has changed AGD will need to drop/clear the table.
# TODO: Recreate table if it doesn't exist (in case AGD drop table instead of just clear it)

start_time = time.time()
performance_terms = search_key_terms(performance, text, "Performance")  # Performance Audit Team Terms
government_terms = search_key_terms(government, text, "Local Government")  # Local Government Audit Team Terms
it_terms = search_key_terms(it, text, "IT")  # IT Audit Team Terms

end_time = time.time()
total_time = end_time - start_time
print(total_time)

# Merge results and output to Excel
merged_data = pd.concat([performance_terms, government_terms, it_terms], ignore_index=True)
merged_data = merged_data.drop_duplicates()  # Drop duplicate rows

print("Combined = ", merged_data.shape)
# Without alternate term search: 17873
# With alternate term search:
merged_data.to_excel('.\\TermSearch.xlsx', sheet_name='TermSearch', index=False)
