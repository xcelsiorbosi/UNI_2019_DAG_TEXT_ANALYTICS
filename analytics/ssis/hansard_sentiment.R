# Load required libraries
library(readxl)
library(tidyr)
library(dplyr)
library(syuzhet)
library(lubridate)
library(sentimentr)
library(ggplot2)
library(tm)
library(RODBC)

options(scipen = 999) # turn off scientific notation

# Import Text and HANSARDFilesInfo tables from HANSARD database
db_connection <- odbcDriverConnect('driver={SQL Server};server=DA-PROD1;database=HANSARD;trusted_connection=true')

text <- sqlQuery(db_connection, "SELECT *  FROM HANSARD.dbo.FinalText")
text$Text <- tolower(text$Text)

info <- sqlQuery(db_connection, "SELECT * FROM HANSARD.dbo.HANSARDFilesInfo")
info <- info[is.na(info$Sentiment),] # Get records without sentiment calculated

text <- text[text$HansardID %in% info$ID,] # Get rows without sentiment calculated

if (nrow(info) > 0) {

  # Combine text transcripts by HansardID
  hansard_text <- text %>% 
    group_by(HansardID) %>% 
    summarise(discussion = paste(Text, collapse = ". "))
    
  # Get raw character vector
  breaked_discussion <- get_sentences(hansard_text$discussion)
    
  # Get sentiment for each Hansard Record
  sentiment_discussion <- sentiment_by(breaked_discussion)
    
  # Add sentiment score to HansardFilesInfo table if it doesn't already exist
  hansard_text$sentiment_score <- sentiment_discussion$ave_sentiment
  hansard_text$discussion <- NULL
  names(hansard_text) <- c("ID", "Sentiment2")
  
  updated_info <- merge(info, hansard_text,by="ID")
  updated_info$Sentiment <- updated_info$Sentiment2
  updated_info$Sentiment2 <- NULL
  
  sqlUpdate(db_connection, updated_info, tablename = "HANSARDFilesInfo")
  
  # Close the database Connection
  odbcClose(db_connection)
    
  # Plot sentiment scores
  #qplot(sentiment_discussion$ave_sentiment, geom="histogram",binwidth=0.05,
  #      main="Hansard Record Sentiment",xlab="Sentiment",ylab="Number of Hansard Records") + 
  #  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
  #        panel.background = element_blank(), axis.line = element_line(colour = "black"))
  
  #summary(sentiment_discussion$ave_sentiment) # Summary statistics for sentiment scores
  
  # https://www.tidytextmining.com/sentiment.html
  # https://towardsdatascience.com/sentiment-analysis-in-r-good-vs-not-good-handling-negations-2404ec9ff2ae
  
  # What positive and negative terms were used to calculate the sentiment for each sentence?
  #terms <- hansard_text$discussion %>% extract_sentiment_terms()
  #head(terms) 
    
  # Sentiment for each sentence
  #sentiment_text <- sentiment(hansard_text$discussion)
  #head(sentiment_text) 

}
  
rm(text, combined, breaked_discussion, hansard_text, info, sentiment_discussion, db_connection)
  