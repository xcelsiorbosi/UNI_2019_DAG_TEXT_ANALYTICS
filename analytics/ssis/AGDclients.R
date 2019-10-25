# Load required libraries
library(readxl)
library(tidyr)
library(dplyr)
library(stringr)
library(RODBC)


# Import Clients and their alternate names from spreadsheet
clients = read_xlsx("C:\\Users\\student2\\Documents\\GitHub\\UNI_2019_DAG_TEXT_ANALYTICS\\data\\ClientNames.xlsx", sheet = "Sheet1")

# Connect to the Text table on the HANSARD SQL Server database
db_connection <- odbcDriverConnect('driver={SQL Server};server=DA-PROD1;database=HANSARD;trusted_connection=true')
text <- sqlQuery(db_connection, "SELECT *  FROM HANSARD.dbo.FinalText")

client_list <- c(clients$AGDClient)

# Text is the record from which column client name is to be searched
search_results <- lapply(client_list, function(client_name) {
  text %>% filter(str_detect(Text, regex(client_name, ignore_case = T))) 
})

# Assign client name to the dataframe
names(search_results) <- client_list

# Create flat file with client name
library(plyr)
search_results <- ldply(search_results, data.frame)
detach(package:plyr)

# Change the column name
names(search_results)[1]<-"AGDClient"

# Merge the client_File and clients to get the Formal Clients and the Client Types
search_results <- merge(x = search_results, y = clients, by = "AGDClient", all.x = TRUE)

# Drop the unnecessary columns and Rownames and renaming the HAnsardID
text_client <- select(search_results, -c("TalkerID", "Text", "Kind", "WordCount"))

# Insert the Data into ClientsMention table in HANSARD database
sqlSave(db_connection, text_client[c("HansardID","TextID","AGDClient","AGDFormal","ClientType")], tablename = "ClientsMention", rownames = FALSE)

# Close the DB Connection
odbcClose(db_connection)