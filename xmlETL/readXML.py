import pyspark 

import sys, os
cwd = os.getcwd()
from pathlib import Path
parentPath = Path(cwd).parent
parentPath = str(parentPath)

xmlLocation = parentPath+"\\Data"
xmlLocationTransformed = parentPath+"\\Data\\transformedXML"
import glob


import xmltodict
import json
from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir(xmlLocation) if isfile(join(xmlLocation, f))]
print(onlyfiles)


## once off trim make this occur after download
for i in onlyfiles:
	with open(xmlLocation+"\\"+i, 'r') as fin:
		data = fin.read().splitlines(True)
	with open(xmlLocationTransformed+"\\"+i, 'w') as fout:
		fout.writelines(data[1:])


import xmltodict
for i in onlyfiles:
	rename = i.split(".")
	rename = rename[0]

	with open(xmlLocationTransformed+"\\"+i) as fd:
		try:
			doc = xmltodict.parse(fd.read())
		except:
			print("nope")
	doc = json.dumps(doc)
	# print(json.dumps(doc))

	with open(parentPath+"\\xml_json\\"+rename+'.json', 'w') as outfile:
		doc = json.loads(doc)
		json.dump(doc, outfile)
		print(doc)