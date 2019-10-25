
#loading requred library
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


#importing text sheet
LDA.Hansard22102019 = read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard22102019.xlsx", sheet = "Text")

#getting header sheet
LDA.HANSARD.header = data.frame(read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard22102019.xlsx", sheet = "Header"))

#Combining all the text transcript by HansardID, Kind and TalkerID
LDA.Hansard.Texts.all = LDA.Hansard22102019 %>% group_by(Kind, TalkerID, HansardID) %>% summarise(discussion = paste(Text, collapse = " "))

#merging talker information and header information
LDA.Hansard.Texts.all = merge(x = LDA.Hansard.Texts.all[,-c(1)], y = LDA.HANSARD.header[,-c(8,10)], 
                          by.x = c("HansardID"), by.y = c("HansardID"))
unique(LDA.Hansard.Texts.all$ProceedingType)

#converting list (Hansard.Texts) into data frame (Hansard.Texts)
LDA.Hansard.bills = filter(LDA.Hansard.Texts.all, LDA.Hansard.Texts.all$ProceedingType == "Bills")

#######################BAsic TEXT ANALYSIS OF DISCUSSION########################

# Build corpus
corpus_bills <- iconv(LDA.Hansard.bills$discussion, to = "UTF-8")
corpus_bills <- Corpus(VectorSource(corpus_bills))

#change to lowercase
Hansard.bills <- tm_map(corpus_bills, content_transformer(tolower))


#remove everything except english words
removeNumPunct <- function(x) gsub("[^[:alpha:][:space:]]*", "", x)
Hansard.bills <- tm_map(Hansard.bills, content_transformer(removeNumPunct))


#removing stop words
Hansard.bills = tm_map(Hansard.bills, removeWords, stop_word) 
#remove whitespace
Hansard.bills <- tm_map(Hansard.bills, stripWhitespace)


#topic Modelling

#importing clean dataset in an matrix form
doc.lengths <- rowSums(as.matrix(DocumentTermMatrix(Hansard.bills)))
dtm <- DocumentTermMatrix(Hansard.bills[doc.lengths > 0])

# Now for some topics
SEED = sample(1:1000000, 1)  # Pick a random seed for replication
k = 5  # Let's start with 5 topics

# This might take a minute!
models <- LDA(dtm, k = k, control = list(seed = SEED))

#list of Topics
terms(models, 10)

#interactive visualization of topic modelling
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
