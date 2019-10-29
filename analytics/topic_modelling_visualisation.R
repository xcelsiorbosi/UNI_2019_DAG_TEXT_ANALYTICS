# Load  required libraries
library(readxl)
library(tidyr)
library(dplyr)
library(openair)
library(syuzhet)
library(lubridate)
library(ggplot2)
library(scales)
library(reshape2)
library(topicmodels)
library(tm)
library(stringr)
library(SnowballC)

project_path = "C:\\Users\\student\\source\\repos\\UNI_2019_DAG_TEXT_ANALYTICS" # UPDATE

input_file = paste(project_path, "\\data\\Hansard22102019.xlsx", sep="")
stopwords_file = paste(project_path, '\\data\\stopwords.txt', sep="")

# Import data from Excel spreadsheet
data = read_xlsx(input_file, sheet = "Text")
header = data.frame(read_xlsx(input_file, sheet = "Header"))

# Combine all text transcripts by HansardID, Kind and TalkerID
text = data %>% group_by(Kind, TalkerID, HansardID) %>% summarise(discussion = paste(Text, collapse = " "))

# Merge talker information and header information
text = merge(x = text[,-c(1)], y = header[,-c(8,10)], by.x = c("HansardID"), by.y = c("HansardID"))
unique(text$ProceedingType)

bills = filter(text, text$ProceedingType == "Bills")

#######################  BASIC TEXT ANALYSIS OF DISCUSSION ########################

# Read stop words from file
stopwords_list = readLines(stopwords_file) 

stop_word <- c(stopwords("english"), "advised", "reply","null", "hon", "january",
               "february", 'march', 'april', 'may', 'minister', 'xhas', 'new','general', 'attorney',
               'june', 'july', 'august', 'september', 'will','since', 'school','picton',
               'october', 'november', 'december','advisedthe', 'stuart�minister',
               'reply', 'can', 'per', 'total', 'many', 'xwhat', 'currently', 'following',
               'australian', 'department','opposition', 'provide','provided', 'including',
               'learning', 'Bill','bill', 'government', 'say', 'well', 'might', 'get','days',
               'want', 'provides', 'like', 'one', 'much', 'look','way', 'know', 'last','today',
               'just', 'two','xthe', 'made','think','within', 'given','place','another',
               'put','take','now','sure','part', 'also', 'advice', 'year', 'number', 'made',
               'think', 'may', 'see', 'able', 'set','better','close','outline','relation','asked','ensure',
               'ask','use','thing','however','quite','put','give','next','question','questions','yesterday',
               'without','every','must', 'whether', 'answer', 'question', 'leave', 'make', 'asking', 'members',
               'explanation', 'brief', 'asking', 'arising', 'seek', 'member', 'interjecting', 'australia',
               'south', 'state', 'regarding', 'house', 'time', 'inform', 'office', 'receive', 'day', 'review',
               'understand','first','croydon�leader','premier', 'years','croydon\xe2leader','staff', stopwords_list)

# Build corpus
corpus_bills <- iconv(bills$discussion, to = "UTF-8")
corpus_bills <- Corpus(VectorSource(corpus_bills))

# Change to lowercase
hansard_bills <- tm_map(corpus_bills, content_transformer(tolower))

# Remove everything except English words
remove_punctuation <- function(x) gsub("[^[:alpha:][:space:]]*", "", x)
hansard_bills <- tm_map(hansard_bills, content_transformer(remove_punctuation))

# Remove stop words
hansard_bills = tm_map(hansard_bills, removeWords, stop_word)

# Remove whitespace
hansard_bills <- tm_map(hansard_bills, stripWhitespace)

# Topic Modelling

# Import clean dataset in an matrix form
doc_lengths <- rowSums(as.matrix(DocumentTermMatrix(hansard_bills)))
dtm <- DocumentTermMatrix(hansard_bills[doc_lengths > 0])

# Now for some topics
SEED = sample(1:1000000, 1)  # Pick a random seed for replication
k = 5  # Let's start with 5 topics
models <- LDA(dtm, k = k, control = list(seed = SEED)) # This might take a minute!

# List of Topics
terms(models, 10)

# Interactive visualisation of topic modelling
topicmodels_json_ldavis <- function(fitted, doc_term){
  require(LDAvis)
  require(slam)
  
  # Find required quantities
  phi <- as.matrix(posterior(fitted)$terms)
  theta <- as.matrix(posterior(fitted)$topics)
  vocab <- colnames(phi)
  term_freq <- slam::col_sums(doc_term)
  
  # Convert to json
  json_lda <- LDAvis::createJSON(phi = phi, theta = theta,
                                 vocab = vocab,
                                 doc.length = as.vector(table(doc_term$i)),
                                 term.frequency = term_freq)
  
  return(json_lda)
}

json_res <- topicmodels_json_ldavis(models, dtm)
serVis(json_res)
