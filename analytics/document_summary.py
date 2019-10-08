# Import all necessary libraries
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer  # is based on The Porter Stemming Algorithm
import numpy as np
import networkx as nx
from gensim.summarization.summarizer import summarize

nltk.download('stopwords')
nltk.download('wordnet')


def smart_truncate(content, length=200, suffix='...'):
    # This function truncates the content to the specified number of characters and appends suffix.
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix


def generate_text_rank_summary(text):
    # Return original text if less than 200 characters long
    if len(text) <= 200:
        return text

    sentences = []
    text_sentences = re.split(r'[?!.] ', text)

    for sentence in text_sentences:
        processed = sentence.replace("[^a-zA-Z]", " ")
        word_count = len(re.findall(r'\w+', processed))
        if word_count > 1:  # Include sentences with more than one word
            sentences.append(processed)

    summary = summarize('. '.join(sentences))
    return summary.replace("\n", " ").replace("..", ".")


# https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
# Approach uses TextRank algorithm
# TextRank does not rely on any previous training data and can work with any arbitrary piece of text.
# TextRank is a general purpose graph-based ranking algorithm for NLP
# Generate clean sentences

# Generate clean sentences
def create_long_sentences(article, output=True):
    sentences = []

    for sentence in article:
        sentence = re.sub(r'[0-9]?.?&#x9;', '', sentence)  # Remove tags
        word_count = len(re.findall(r'\w+', sentence))
        if 4 < word_count <= 100:  # Include sentences with 5 to 100 words
            sentences.append(sentence.split(" "))
        if output:
            print(sentence, ": words = ", word_count)

    return sentences


# Process word by converting to lowercase, removing punctuation, lemmatising, and stemming.
# https://medium.com/@pemagrg/pre-processing-text-in-python-ad13ea544dae
def process_word(word):
    wordnet_lemmatizer = WordNetLemmatizer()
    snowball_stemmer = SnowballStemmer('english')

    word = word.lower()  # convert to lowercase
    word = word.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    word = wordnet_lemmatizer.lemmatize(word)  # lemmatise words
    word = snowball_stemmer.stem(word)  # stemming

    return word


# Process sentence by converting to lowercase, removing punctuation, lemmatising, stemming and removing stopwords.
# Sentence must be a list of words that make up the sentence
# https://medium.com/@pemagrg/pre-processing-text-in-python-ad13ea544dae
def process_sentence(sentence):
    # Process words in sentence
    processed_sentence = [process_word(word) for word in sentence]

    # Remove stopwords
    stop_words = stopwords.words('english')
    processed_sentence = [word for word in processed_sentence if word not in stop_words]

    return processed_sentence


# Similarity matrix
def sentence_similarity(sent1, sent2):
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        vector2[all_words.index(w)] += 1

    # Vectors must be non-zero to calculate cosine similarity
    if np.count_nonzero(vector1) == 0 or np.count_nonzero(vector2) == 0:
        return 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    processed_sentences = [process_sentence(sentence) for sentence in sentences]

    for idx1 in range(len(processed_sentences)):
        for idx2 in range(len(processed_sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            sentences_similarity = sentence_similarity(processed_sentences[idx1], processed_sentences[idx2])
            similarity_matrix[idx1][idx2] = sentences_similarity

    return similarity_matrix


# Generate Summary Method
def generate_summary_from_file(file_path, top_n=5, output=True):
    # Read text and split it into sentences
    file = open(file_path, "r")
    file_data = file.readlines()
    sentences = re.split(r'[?!.] ', file_data[0])

    long_sentences = create_long_sentences(sentences, output)
    return generate_summary(long_sentences, top_n, output)


def generate_summary_from_text(text, top_n=5, output=True):
    if len(text) <= 200:
        # If text is short, return the original text rather than a summary
        return text
    else:
        # Read text and split it into sentences
        sentences = re.split(r'[?!.] ', text)
        long_sentences = create_long_sentences(sentences, output)
        return generate_summary(long_sentences, top_n, output)


def generate_summary(sentences, top_n=5, output=True):
    summarize_text = []

    # Generate Similarly Matrix across sentences
    sentence_similarity_matrix = build_similarity_matrix(sentences)

    # Rank sentences in similarity matrix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    try:
        # https://stackoverflow.com/questions/13040548/networkx-differences-between-pagerank-pagerank-numpy-and-pagerank-scipy
        # The eigenvector calculation uses NumPy’s interface to the LAPACK eigenvalue solvers.
        # This will be the fastest and most accurate for small graphs.
        scores = nx.pagerank_numpy(sentence_similarity_graph)
    except nx.NetworkXError:
        print("NetworkXError")
        return ""
    except nx.PowerIterationFailedConvergence:
        print("PowerIterationFailedConvergence")
        return ""

    # Sort the rank and pick top sentences
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    if output:
        print("Indexes of top ranked_sentence order are ", ranked_sentences)

    if len(ranked_sentences) < top_n:
        top_n = len(ranked_sentences)

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentences[i][1]))

    # Output the summary text
    return '. '.join(summarize_text).replace("..", ".")
