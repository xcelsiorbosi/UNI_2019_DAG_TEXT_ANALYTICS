import os
from pathlib import Path
import json
from os import listdir
from os.path import isfile, join

cwd = os.getcwd()
parentPath = Path(cwd).parent
parentPath = str(parentPath)

xmlLocation = parentPath + "\\data"
xmlLocationTransformed = parentPath + "\\data\\transformedXML"

only_files = [f for f in listdir(xmlLocation) if isfile(join(xmlLocation, f))]
print(only_files)

# once off trim - make this occur after download
for i in only_files:
    with open(xmlLocation + "\\" + i, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(xmlLocationTransformed + "\\" + i, 'w') as fout:
        fout.writelines(data[1:])

import xmltodict

for i in only_files:
    rename = i.split(".")
    rename = rename[0]

    with open(xmlLocationTransformed + "\\" + i) as fd:
        try:
            doc = xmltodict.parse(fd.read())
        except:
            print("Exception")
    doc = json.dumps(doc)
    # print(json.dumps(doc))

    with open(parentPath + "\\xml_json\\" + rename + '.json', 'w') as outfile:
        doc = json.loads(doc)
        json.dump(doc, outfile)
        print(doc)
