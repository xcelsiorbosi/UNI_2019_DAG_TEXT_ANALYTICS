import re
from gensim.summarization import keywords


# This function counts the number of words in provided text
def word_count(text):
    return len(re.findall(r'\w+', text))


# This function gets the comma separated keywords of the text to a maximum number of words.
# Words are lemmatised and accentuation removed.
def get_keywords(text, words_returned=10):
    keyword_list = keywords(text, split=True, lemmatize=True, deacc=True)
    return ', '.join(keyword_list[:words_returned])
