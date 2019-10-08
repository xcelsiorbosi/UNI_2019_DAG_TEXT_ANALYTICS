# Load required libraries
library(readxl)
library(tidyr)
library(dplyr)
library(syuzhet)
library(lubridate)
library(sentimentr)

setwd("D:/Education/2015-2019 - Master of Data Science/2019-S2 - Capstone Professional Project/Project Code")

# Import Text sheet
data = read_xlsx("./data/Hansard1102019.xlsx", sheet = "Text")
head(data)

# Import HANSARDFilesInfo sheet
#HANSARDFilesInfo = data.frame(read_xlsx("./data/Hansard1102019.xlsx", sheet = "HANSARDFilesInfo"))
#head(HANSARDFilesInfo)

# Combine text transcripts by HansardID
hansard_text = data %>% 
  #group_by(Kind,TalkerID,HansardID) %>% 
  group_by(HansardID) %>% 
  summarise(discussion = paste(Text, collapse = ". "))
head(hansard_text)

# Merge talker information and file information
#hansard_text = data.frame(merge(x=hansard_text, y=HANSARDFilesInfo[,-c(1,4)], 
#                                     by.x = "HansardID", by.y = "FileName"))
#hansard_text$URL <- NULL
#str(hansard_text)

rm(data) # remove unneeded data

# Get raw character vector
breaked_discussion = get_sentences(hansard_text$discussion)

# Get sentiment for each Hansard Record
sentiment_discussion = sentiment_by(breaked_discussion)
head(sentiment_discussion)

# Export sentiment score as CSV
hansard_text$sentiment_score = sentiment_discussion$ave_sentiment
hansard_text$discussion <- NULL
names(hansard_text) <- c("FileName", "SentimentScore")
write.csv(hansard_text, "./analytics/HansardRecordSentiment.csv", row.names = FALSE)

rm(breaked_discussion, hansard_text, sentiment_discussion)

# https://www.tidytextmining.com/sentiment.html
# https://towardsdatascience.com/sentiment-analysis-in-r-good-vs-not-good-handling-negations-2404ec9ff2ae
# https://www.datacamp.com/community/tutorials/sentiment-analysis-R
# https://www.kaggle.com/rtatman/tutorial-sentiment-analysis-in-r