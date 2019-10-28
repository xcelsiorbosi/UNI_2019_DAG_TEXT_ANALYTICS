# nltk.download('punkt')
import pandas as pd
from nltk.tokenize import word_tokenize


try: 
	wordLoopUp = pd.read_csv('wordLookUp.csv')
except:
	wordLoopUp = pd.DataFrame(None, columns=["word", "wordID"])
	wordLoopUp.to_csv('wordLookUp.csv')

try: 
	wordHansardLookUp = pd.read_csv('wordHansardLookUp.csv')
except:
	wordHansardLookUp = pd.DataFrame(None, columns=["word", "textID"])
	wordHansardLookUp.to_csv('wordHansardLookUp.csv')

from nltk.tokenize import sent_tokenize
df = pd.read_excel("..\\data\\Hansard22102019.xlsx")
# print(df.head())

dfTemp = df
print(dfTemp.columns)

sentTokens = []
# for i in dfTemp['talkerTranscript']:
for i in dfTemp['Text']:
    try:
        a = sent_tokenize(i)
        sentTokens.append(a)
        # print(a)
    except:
        print("error")
        sentTokens.append("blank")

loops = len(sentTokens)

def clean(sent):
	sent = sent.replace(".","")
	sent = sent.replace("/","")
	sent = sent.replace("*","")
	sent = sent.replace(":","")
	sent = sent.replace(",","")
	sent = sent.replace("'","")
	sent = sent.replace('"',"")
	sent = sent.replace("|","")
	sent = sent.replace("\\","")
	sent = sent.replace("/","")
	sent = sent.replace("#","")
	sent = sent.replace("@","")
	sent = sent.replace("%","")
	sent = sent.replace("(","")
	sent = sent.replace(")","")

	sent = sent.replace("!","")
	sent = sent.replace("#","")
	sent = sent.replace("$","")	
	sent = sent.replace("%","")
	sent = sent.replace("^","")
	sent = sent.replace("&","")
	sent = sent.replace("*","")	
	sent = sent.replace("?","")
	sent = sent.replace("<","")
	sent = sent.replace(">","")
	sent = sent.replace(";","")	
	sent = sent.replace("+","")
	sent = sent.lower()

	return sent


def check_bag(listOfWordTokens, TextID):
	# print(listOfWordTokens)
	for i in listOfWordTokens:
		dfTempBagOfWords = pd.read_csv('wordLookUp.csv')
		wordHansardLookUp = pd.read_csv('wordHansardLookUp.csv')
		wordIDs = list(dfTempBagOfWords["wordID"])
		currentWords = list(dfTempBagOfWords["word"])
		records = int(len(dfTempBagOfWords))
		currentWord = i
		try:
			loc = currentWords.index(i)
			print(loc)

			#word and textID
			wordLocAndWord = [currentWord, TextID]
			# newFrameTextToTextID = pd.DataFrame([wordLocAndWord],columns = ["wordID", "textID"])

			tempwordHansardLookUp = wordHansardLookUp.append(newFrameTextToTextID)
			tempwordHansardLookUp = tempwordHansardLookUp.drop_duplicates()
			# tempwordHansardLookUp = tempwordHansardLookUp.reset_index()
			tempwordHansardLookUp.to_csv('wordHansardLookUp.csv', index=False)
		except:
			word_id = 	records + 1
			print('adding to wordBank')
			# wordIDs.append(word_id)
			
			# word and bagofwords
			thing = [currentWord, word_id]
			newFrame = pd.DataFrame([thing],columns = ['word', 'wordID'])
			tempBagofwords = dfTempBagOfWords.append(newFrame)

			# word and textID
			wordLocAndWord = [currentWord, TextID]
			newFrameTextToTextID = pd.DataFrame([wordLocAndWord],columns = ["word", "textID"])
			tempwordHansardLookUp = wordHansardLookUp.append(newFrameTextToTextID)

			print("-------------------------------")
			print(tempBagofwords)
			tempBagofwords = tempBagofwords.drop_duplicates()
			# tempBagofwords = tempBagofwords.reset_index()
			tempBagofwords.to_csv('wordLookUp.csv', index=False)
			print("-------------------------------")
			tempwordHansardLookUp = tempwordHansardLookUp.drop_duplicates()
			# tempwordHansardLookUp = tempwordHansardLookUp.reset_index()
			tempwordHansardLookUp.to_csv('wordHansardLookUp.csv', index=False)
			print(tempwordHansardLookUp)
			print("-------------------------------")

for i in range(loops):
	wordTokens = []
	cleanSent = clean(sentTokens[i][0])
	a = word_tokenize(cleanSent)
	# print(a)
	wordTokens.append(a)
	textID = df['TextID'][i]
	for j in wordTokens:
		check_bag(j,textID)

# import pandas as pd
# df = pd.read_excel("..\\data\\Hansard22102019.xlsx")
# print(df['TextID'][8])
