# Import all necessary libraries
import nltk
import re
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from gensim.summarization.summarizer import summarize

nltk.download('stopwords')


def smart_truncate(content, length=200, suffix='...'):
    # This function truncates the content to the specified number of characters and appends suffix.
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix


def generate_text_rank_summary(original_text):
    # Return original text if it less than 200 characters long
    if len(original_text) <= 200:
        return original_text

    sentences = []
    text = re.split(r'[?!.] ', original_text)

    for sentence in text:
        processed = sentence.replace("[^a-zA-Z]", " ")
        word_count = len(re.findall(r'\w+', processed))

        # Include sentences containing more than one word in summary
        if word_count > 1:
            sentences.append(processed)

    text = '. '.join(sentences)

    summary = summarize(text)
    return summary.replace("\n", " ").replace("..", ".")


# https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
# Approach uses TextRank algorithm
# TextRank does not rely on any previous training data and can work with any arbitrary piece of text.
# TextRank is a general purpose graph-based ranking algorithm for NLP
# Generate clean sentences
def read_article(file_name, output=True):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = re.split(r'[?!.:] ', filedata[0])
    return create_clean_sentences(article, output)


def read_text(text, output=True):
    article = re.split(r'[?!.:] ', text)
    return create_clean_sentences(article, output)


def create_clean_sentences(article, output=True):
    sentences = []

    for sentence in article:
        processed = sentence.replace("[^a-zA-Z]", " ")
        word_count = len(re.findall(r'\w+', processed))
        if word_count > 4:  # Include sentences with more than five words
            sentences.append(processed.split(" "))
        if output:
            print(sentence, ": words = ", word_count)

    # sentences.pop()

    return sentences


# Similarity matrix
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


# Generate Summary Method
def generate_summary(file_name, text, top_n=5, output=True):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text and split it
    sentences = ""
    if file_name is not None:
        sentences = read_article(file_name, output)
    elif len(text) <= 200:
        # If text is short don't return a summary. Return the text
        return text
    else:
        sentences = read_text(text, output)

    # Step 2 - Generate Similarly Matrix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity matrix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    try:
        scores = nx.pagerank(sentence_similarity_graph, max_iter=100)
    except nx.NetworkXError:
        return ""
    except nx.PowerIterationFailedConvergence:
        return ""

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    if output:
        print("Indexes of top ranked_sentence order are ", ranked_sentence)

    if len(ranked_sentence) < top_n:
        top_n = len(ranked_sentence)

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - output the summary text
    return '. '.join(summarize_text).replace("..", ".")
