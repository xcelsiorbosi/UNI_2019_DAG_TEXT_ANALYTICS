import re
from gensim.summarization import keywords


def word_count(text):
    # This function counts the number of words in provided text
    return len(re.findall(r'\w+', text))


def get_keywords(text):
    # This function gets the comma separated keywords of the text.
    # Words are lemmatised and accentuation removed.
    return keywords(text, lemmatize=True, deacc=True).replace("\n", ", ")
