#loading requred library
library(readxl)
library(tidyr)
library(dplyr)
library(stringr)
library(RODBC)


#importing Clients table
clients = read_xlsx("C:\\Users\\student2\\Desktop\\Clients_mention_Dashboard_Re_Moe\\Clients12102019.xlsx", sheet = "Sheet1")
#Connecting to the Text table on the SQL Server DB

dbhandle <- odbcDriverConnect('driver={SQL Server};server=DA-PROD1;database=HANSARD;trusted_connection=true')
currTableSQL<-paste("SELECT *  FROM HANSARD.dbo.FinalText",sep="")

Hansard1102019 <-sqlQuery(dbhandle,currTableSQL)


clientlist <- c(clients$AGDClient)

#here header is the dataframe where we need to search for client name
# discussion is the texts from which column cleint name is to be searched

dataframe_list <- lapply(clientlist, function(clientName) {
  Hansard1102019 %>% filter(str_detect(Text, regex(clientName, ignore_case = T))) 
})

#assigning client name to the dataframe
names(dataframe_list) <- clientlist

#flat file with client name
library(plyr)
Client_File <- ldply(dataframe_list, data.frame)
detach(package:plyr)

#Changing the column name
names(Client_File)[1]<-"AGDClient"

# Merging the client_File and clients to get the Formal Clients and the Client Types
TextClient1 <- merge(x = Client_File, y = clients, by = "AGDClient", all.x = TRUE)

# Dropping the unnecessary columns and Rownames and renaming the HAnsardID

TextClient <- select(TextClient1, -c("TalkerID", "Text", "Kind","WordCount"))

#names(TextClient)[3]<-"FileName"

# Inserting the Data into clientsmention table on Hansard DB on SS
sqlSave(dbhandle, TextClient[c("HansardID","TextID","AGDClient","AGDFormal","ClientType")], tablename = "ClientsMention",rownames = FALSE)

#Closing the DB Connection
odbcClose(dbhandle)