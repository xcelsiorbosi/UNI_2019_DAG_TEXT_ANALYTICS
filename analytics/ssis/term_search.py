import pandas as pd
import numpy as np


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

    # Search for terms separated by '+' in any order:
    # Use regex (?=.*\bTerm\b)(?=.*\bTerm\b) where \b is a word boundary
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
            match_alternate = match['Term'] | \
                              text_df.TextLower.str.contains(row['AlternatePattern'], case=False, regex=True) | \
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

