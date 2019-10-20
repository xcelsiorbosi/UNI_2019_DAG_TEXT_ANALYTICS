#loading required library
library(textmineR)
library(tm)
library(readxl)
library(tidyr)
library(dplyr)
library(stringr)
library(SnowballC)
library(textclean)
library(stopwords)
#importing text sheet
LDA.Hansard1102019 = read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "Text")

#importing talker staging sheet
TalkerStaging = read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", 
                          sheet = "TalkerStaging")

Talker = unique(TalkerStaging$TalkerName)
#Talker = paste0('"',Talker,'"')
Electorate=unique(TalkerStaging$Electorate)

#path = ("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx")

LDA.Hansard1102019 = LDA.Hansard1102019 %>% filter(LDA.Hansard1102019$Kind != "NULL")

listofphrase = c("The PRESIDENT:  Minister.", "Leave granted.","Members interjecting:", "The SPEAKER:  Order!", 
                 "The SPEAKER:", "interjecting:", "NULL","The PRESIDENT:","The CHAIR:")

#removing rows that has above list of phrase
LDA.Hansard1102019 = drop_row(LDA.Hansard1102019, "Text", listofphrase,  ignore.case=TRUE)
#LDA.Hansard1102019$Text = str_replace(LDA.Hansard1102019$Text, "The Hon.*:","")

#removing talker names
LDA.Hansard1102019$Text <- gsub(paste0(Talker,collapse = "|"),"", LDA.Hansard1102019$Text)

#removing Electorate information
LDA.Hansard1102019$Text <- gsub(paste0(Electorate,collapse = "|"),"", LDA.Hansard1102019$Text)


#Question Kind
LDA.Hansard.question = filter(LDA.Hansard1102019, LDA.Hansard1102019$Kind == "question")

#Stop word "stopwords.txt" file location from database

listofStopWords = readLines('C:\\Users\\Bipin Karki\\Desktop\\stopwords.txt') 

stop_word <- c(stopwords("english"), "advised", "reply","null", "hon", "january",
               "february", 'march', 'april', 'may', 'minister', 'xhas', 'new','general', 'attorney',
               'june', 'july', 'august', 'september', 'will','since', 'school','picton',
               'october', 'november', 'december','advisedthe', 'stuartâminister',
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
               'understand','first','croydonâleader','premier', 'years','croydon\xe2leader','staff', listofStopWords)


dtm <- CreateDtm(doc_vec = LDA.Hansard.question$Text, # character vector of documents
                 
                 ngram_window = c(1, 2), # minimum and maximum n-gram length
                 stopword_vec = c(stopwords::stopwords("en"), # stopwords from tm
                                  stopwords::stopwords(source = "smart"),stop_word), # this is the default value
                 lower = TRUE, # lowercase - this is the default value
                 remove_punctuation = TRUE, # punctuation - this is the default
                 remove_numbers = TRUE, # numbers - this is the default
                 verbose = FALSE, # Turn off status bar for this demo
                 cpus = 2) # default is all available cpus on the system

question.dtm <- dtm[,colSums(dtm) > 1]

#das = CreateDtm(Hansard.question)
# Fit a Latent Dirichlet Allocation model
# choose a range of k 
# - here, the range runs into the corpus size.
k_list <- seq(5,50, by=10)

#With a decent sized corpus, the procedure can take hours or days, 
# depending on the size of the data and complexity of the model.

model_dir <- paste0("models_", digest::digest(colnames(question.dtm), algo = "sha1"))

# Fit a bunch of LDA models
model_list <- TmParallelApply(X = k_list, FUN = function(k){
  
  m <- FitLdaModel(dtm = question.dtm, 
                   k = k, 
                   iterations = 200, 
                   burnin = 180,
                   alpha = 0.1,
                   beta = colSums(question.dtm) / sum(question.dtm) * 100,
                   optimize_alpha = TRUE,
                   calc_likelihood = FALSE,
                   calc_coherence = TRUE,
                   calc_r2 = FALSE,
                   cpus = 1)
  m$k <- k
  
  m
}, export= ls(), # c("question.dtm"), # export only needed for Windows machines
cpus = 2) 

# Get average coherence for each model
coherence_mat <- data.frame(k = sapply(model_list, function(x) nrow(x$phi)), 
                            coherence = sapply(model_list, function(x) mean(x$coherence)), 
                            stringsAsFactors = FALSE)

new_coherence_mat = coherence_mat %>% filter(k, k<31)
optimum_coherence = new_coherence_mat[which.max(new_coherence_mat$coherence),]
numerofTopics = optimum_coherence[,1]

# Plot the result
# On larger (~1,000 or greater documents) corpora, you will usually get a clear peak
'
plot(coherence_mat, type = "o", col = "red", xlab = "Number of Topics", ylab = "Coherence score", 
     main = "Coherence plot for K Topics", pch = 16, cex = 1)
axis(1, seq(0,85,10))
abline(v=seq(0,85,10), lty=3, col="gray")

'
set.seed(12345)

model <- FitLdaModel(dtm = question.dtm, 
                     k = numerofTopics,
                     iterations = 500, # I usually recommend at least 500 iterations or more
                     burnin = 180,
                     alpha = 0.1,
                     beta = 0.05,
                     optimize_alpha = TRUE,
                     calc_likelihood = TRUE,
                     calc_coherence = TRUE,
                     calc_r2 = TRUE,
                     cpus = 2) 

# Get the top terms of each topic
model$top_terms <- GetTopTerms(phi = model$phi, M = 25)

# Get the prevalence of each topic
# You can make this discrete by applying a threshold, say 0.05, for
# topics in/out of docuemnts. 
model$prevalence <- colSums(model$theta) / sum(model$theta) * 100

# prevalence should be proportional to alpha
#plot(model$prevalence, model$alpha, xlab = "prevalence", ylab = "alpha")

# topic labeling tool based on probable bigrams
model$labels <- LabelTopics(assignments = model$theta > 0.05, 
                                      dtm = question.dtm,
                                      M = 1)

#head(model$labels, 25)

# put them together, with coherence into a summary table
model$summary <- data.frame(topic = rownames(model$phi),
                            label = model$labels,
                            coherence = round(model$coherence, 3),
                            prevalence = round(model$prevalence,3),
                            top_terms = apply(model$top_terms, 2, function(x){
                              paste(x, collapse = ", ")
                            }),
                            stringsAsFactors = FALSE)

TopicsTopWords = as.data.frame(model$summary[ order(model$summary$prevalence, decreasing = TRUE) , ][ 1:numerofTopics , ])

Export_TopicsTopWords = TopicsTopWords[,c(2,4,5)]
colnames(Export_TopicsTopWords) = c('Topic Labels', 'Prevalence', 'Top related words')
#Export to Database
write.csv(Export_TopicsTopWords, "TopicsTopWords.csv")

#interactive visualization of topic modelling
library(LDAvis)
require(slam)
json <- createJSON(phi = model$phi,
                   theta = model$theta,
                   doc.length = row_sums(question.dtm),
                   vocab = colnames(question.dtm),
                   term.frequency = col_sums(question.dtm))

#location to export html file in database
serVis(json, out.dir = "C:\\Users\\Bipin Karki\\Desktop\\question")
