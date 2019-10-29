# Load required libraries
library(textmineR)
library(tm)
library(readxl)
library(tidyr)
library(dplyr)
library(stringr)
library(SnowballC)
library(textclean)
library(stopwords)

project_path = "C:\\Users\\student\\source\\repos\\UNI_2019_DAG_TEXT_ANALYTICS" # UPDATE

input_file = paste(project_path, "\\data\\Hansard22102019.xlsx", sep="")
stopwords_file = paste(project_path, '\\data\\stopwords.txt', sep="")
output_directory = paste(project_path, "\\analytics", sep="")

# Import text sheet
data = read_xlsx(input_file, sheet = "Text")

# Import Talker Staging sheet
talker_staging = read_xlsx(input_file, sheet = "TalkerStaging")

talker = unique(talker_staging$TalkerName)
electorate=unique(talker_staging$Electorate)

data = data %>% filter(data$Kind != "NULL")

phrase_list = c("The PRESIDENT:  Minister.", "Leave granted.","Members interjecting:", "The SPEAKER:  Order!", 
                 "The SPEAKER:", "interjecting:", "NULL","The PRESIDENT:","The CHAIR:")

# Remove rows that contain above list of phrases
data = drop_row(data, "Text", phrase_list,  ignore.case=TRUE)
#data$Text = str_replace(data$Text, "The Hon.*:","")

# Remove talker names
data$Text <- gsub(paste0(talker,collapse = "|"),"", data$Text)

# Remove Electorate information
data$Text <- gsub(paste0(electorate,collapse = "|"),"", data$Text)

# Question Kind
hansard_question = filter(data, data$Kind == "question")

# Stop word "stopwords.txt" file location from database
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


dtm <- CreateDtm(doc_vec = hansard_question$Text, # character vector of documents
                 
                 ngram_window = c(1, 2), # minimum and maximum n-gram length
                 stopword_vec = c(stopwords::stopwords("en"), # stopwords from tm
                                  stopwords::stopwords(source = "smart"),stop_word), # this is the default value
                 lower = TRUE, # lowercase - this is the default value
                 remove_punctuation = TRUE, # punctuation - this is the default
                 remove_numbers = TRUE, # numbers - this is the default
                 verbose = FALSE, # Turn off status bar for this demo
                 cpus = 2) # default is all available cpus on the system

question_dtm <- dtm[,colSums(dtm) > 1]

#das = CreateDtm(Hansard.question)
# Fit a Latent Dirichlet Allocation model
# choose a range of k 
# - here, the range runs into the corpus size.
k_list <- seq(5,50, by=10)

# With a decent sized corpus, the procedure can take hours or days, 
# depending on the size of the data and complexity of the model.
model_dir <- paste0("models_", digest::digest(colnames(question_dtm), algo = "sha1"))

# Fit a bunch of LDA models
model_list <- TmParallelApply(X = k_list, FUN = function(k){
  
  m <- FitLdaModel(dtm = question_dtm, 
                   k = k, 
                   iterations = 200, 
                   burnin = 180,
                   alpha = 0.1,
                   beta = colSums(question_dtm) / sum(question_dtm) * 100,
                   optimize_alpha = TRUE,
                   calc_likelihood = FALSE,
                   calc_coherence = TRUE,
                   calc_r2 = FALSE,
                   cpus = 1)
  m$k <- k
  m
}, export = ls(), # c("question_dtm"), # export only needed for Windows machines
cpus = 2) 

# Get average coherence for each model
coherence_mat <- data.frame(k = sapply(model_list, function(x) nrow(x$phi)), 
                            coherence = sapply(model_list, function(x) mean(x$coherence)), 
                            stringsAsFactors = FALSE)

new_coherence_mat = coherence_mat %>% filter(k, k<31)
optimum_coherence = new_coherence_mat[which.max(new_coherence_mat$coherence),]
number_topics = optimum_coherence[,1]

# Plot the result
# On larger (~1,000 or greater documents) corpora, you will usually get a clear peak
'
plot(coherence_mat, type = "o", col = "red", xlab = "Number of Topics", ylab = "Coherence score", 
     main = "Coherence plot for K Topics", pch = 16, cex = 1)
axis(1, seq(0,85,10))
abline(v=seq(0,85,10), lty=3, col="gray")
'
set.seed(12345)

model <- FitLdaModel(dtm = question_dtm, 
                     k = number_topics,
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
# topics in/out of documents 
model$prevalence <- colSums(model$theta) / sum(model$theta) * 100

# Prevalence should be proportional to alpha
#plot(model$prevalence, model$alpha, xlab = "prevalence", ylab = "alpha")

# topic labeling tool based on probable bigrams
model$labels <- LabelTopics(assignments = model$theta > 0.05, 
                                      dtm = question_dtm,
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

topics_top_words = as.data.frame(model$summary[ order(model$summary$prevalence, decreasing = TRUE) , ][ 1:number_topics , ])

export_topics_top_words = topics_top_words[,c(2,4,5)]
colnames(export_topics_top_words) = c('Topic Labels', 'Prevalence', 'Top related words')

# Export to CSV
write.csv(export_topics_top_words, "TopicsTopWords.csv")

# Interactive visualisation of topic modelling
library(LDAvis)
require(slam)
json <- createJSON(phi = model$phi,
                   theta = model$theta,
                   doc.length = row_sums(question_dtm),
                   vocab = colnames(question_dtm),
                   term.frequency = col_sums(question_dtm))

# Location to export html file in database
serVis(json, out.dir = output_directory)
