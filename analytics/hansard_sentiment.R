# Load required libraries
library(readxl)
library(tidyr)
library(dplyr)
library(syuzhet)
library(lubridate)
library(sentimentr)
library(ggplot2)

options(scipen = 999) # turn off scientific notation

setwd("D:/Education/2015-2019 - Master of Data Science/2019-S2 - Capstone Professional Project/Project Code")

# Import Text sheet
data = read_xlsx("./data/HansardText10102019.xlsx", col_types = "text")
head(data)
head(data[data$HansardID == "HANSARD-11-27883.xml",]) # Check TextID is no longer using scientific notation

# Get Sentiment for each Hansard ID
   
  # Combine text transcripts by HansardID
  hansard_text = data %>% 
    group_by(HansardID) %>% 
    summarise(discussion = paste(Text, collapse = ". "))
  head(hansard_text)
  
  # Get raw character vector
  breaked_discussion = get_sentences(hansard_text$discussion)
  
  # Get sentiment for each Hansard Record
  sentiment_discussion = sentiment_by(breaked_discussion)
  head(sentiment_discussion)
  
  # Export sentiment score as CSV
  hansard_text$sentiment_score = sentiment_discussion$ave_sentiment
  hansard_text$sentiment_score_sd = sentiment_discussion$sd
  hansard_text$discussion <- NULL
  names(hansard_text) <- c("FileName", "SentimentScore", "SentimentScoreSD")
  write.csv(hansard_text, "./analytics/HansardRecordSentiment.csv", row.names = FALSE)
  
  qplot(sentiment_discussion$ave_sentiment, geom="histogram",binwidth=0.05,
        main="Hansard Record Sentiment",xlab="Sentiment",ylab="Number of Hansard Records")
  summary(sentiment_discussion$ave_sentiment)

# Get Sentiment for each Text ID

  hansard_text = data %>% 
    group_by(TextID, HansardID) %>% 
    summarise(discussion = paste(Text, collapse = ". "))
  head(hansard_text)
  
  # Get raw character vector
  breaked_discussion = get_sentences(hansard_text$discussion)
  
  # Get sentiment for each Hansard Record
  sentiment_discussion = sentiment_by(breaked_discussion)
  head(sentiment_discussion)
  
  # Export sentiment score as CSV
  hansard_text$sentiment_score = sentiment_discussion$ave_sentiment
  hansard_text$sentiment_score_sd = sentiment_discussion$sd
  hansard_text$discussion <- NULL
  names(hansard_text) <- c("TextID","FileName", "SentimentScore", "SentimentScoreSD")
  head(hansard_text)
  write.csv(hansard_text, "./analytics/HansardTextSentiment.csv", row.names = FALSE)
  
  qplot(sentiment_discussion$ave_sentiment, geom="histogram",binwidth=0.05,
        main="Hansard Text Sentiment",xlab="Sentiment",ylab="Number of Text Fragments")
  summary(sentiment_discussion$ave_sentiment)

rm(data, breaked_discussion, hansard_text, sentiment_discussion)

# https://www.tidytextmining.com/sentiment.html
# https://towardsdatascience.com/sentiment-analysis-in-r-good-vs-not-good-handling-negations-2404ec9ff2ae
# https://www.datacamp.com/community/tutorials/sentiment-analysis-R
# https://www.kaggle.com/rtatman/tutorial-sentiment-analysis-in-r
# https://medium.com/@mattifuchs/doing-your-first-sentiment-analysis-in-r-with-sentimentr-167855445132