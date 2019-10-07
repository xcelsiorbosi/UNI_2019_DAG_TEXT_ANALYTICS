#loading requred library
library(readxl)
library(tidyr)
library(dplyr)
library(syuzhet)
library(lubridate)
library(sentimentr)


#importing text sheet
Hansard_1102019 = read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "Text")

#getting HANSARDfilesinfo sheet
HANSARDFilesInfo = data.frame(read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "HANSARDFilesInfo"))


#Combining all the text transcript by HansardID, Kind and TalkerID
Hansard.Texts = Hansard_1102019 %>% group_by(Kind, TalkerID, HansardID) %>% summarise(discussion = paste(Text, collapse = " "))


#merging talker information and file information
Hansard.Texts = data.frame(merge(x=Hansard.Texts, y=HANSARDFilesInfo[,-c(1,4)], 
                                     by.x = "HansardID", by.y = "FileName"))


#Getting raw character vector
breaked_discussion = get_sentences(Hansard.Texts.all$discussion)

#fetching sentiments
Sentiment.discussion =  sentiment_by(breaked.discussion)

#this adds sentiment score in the dataframe
Hansard.Texts.all$sentiment_score = Sentiment.discussion$ave_sentiment
write.csv(Hansard.Texts.all,"C:\\Users\\Bipin Karki\\Desktop\\Hansard.sentiment.csv")

