import pyspark 

import sys, os
cwd = os.getcwd()
from pathlib import Path
parentPath = Path(cwd).parent
parentPath = str(parentPath)

xmlLocation = parentPath+"\\Data"
import glob


import xmltodict
import json
from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir(xmlLocation) if isfile(join(xmlLocation, f))]
print(onlyfiles)


## once off trim make this occur after download
# for i in onlyfiles:
# 	with open(xmlLocation+"\\"+i, 'r') as fin:
# 		data = fin.read().splitlines(True)
# 	with open(xmlLocation+"\\"+i, 'w') as fout:
# 		fout.writelines(data[1:])


import xmltodict
for i in onlyfiles:
	rename = i.split(".")
	rename = rename[0]

	with open(xmlLocation+"\\"+i) as fd:
		try:
			doc = xmltodict.parse(fd.read())
		except:
			print("nope")
	doc = json.dumps(doc)
	# print(json.dumps(doc))

	with open(parentPath+"\\xml_json\\"+rename+'.json', 'w') as outfile:
		json.dump(doc, outfile)
	# json_transform = json.loads(jsojson.dumps(dic)n.dumps(xmltodict.parse(i, process_namespaces=True)))

	# print(json_transform)

# mydict = {u'root': {u'persons': [{u'@city': u'hyderabad', u'person': {u'@name': u'abc', u'name': {u'@mobile': u'789', u'@age': u'50'}}}, {u'@city': u'vizag', u'person': {u'@name': u'xyz', u'name': {u'@mobile': u'123', u'@age': u'70'}}}]}}
# print (xmltodict.unparse(mydict, pretty=True))


# .option("rowTag", "foo").load(parentPath+"\\Data"")
