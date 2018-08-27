import os
import sys
import json
import pandas as pd
import multiprocessing
import xml.etree.ElementTree as ET


if(len(sys.argv))>=5:
	INPUT=sys.argv[1]+"/"
	PATH=sys.argv[2]+"/"
	CANONICAL=sys.argv[3]
	CORR_NAME=sys.argv[4]
else:
	print ("USAGE: {} INPUT_FOL PATH_OUT CANONICAL_FILE CORRESPONDENCE_FILE".format(sys.argv[0]))
	sys.exit()

with open(CORR_NAME, "r") as f:
	correspondence=json.loads(f.readline())


def generateMatrix(fout, df):
	global CANONICAL
	e = ET.parse(CANONICAL)
	root=e.getroot()
	for child in root:
		if child.tag=="layer":
			for item in child:
				if item.tag=="demand":
					iin=correspondence.get(item.get("ingressNodeId"))
					out=correspondence.get(item.get("egressNodeId"))
					print("INPUT NODE: {}; output: {}".format(iin, out))
					df.index=[str(ind) for ind in df.index.values]
					item.set("offeredTraffic", str(df.loc[str(iin), str(out)]))
	e.write(fout, xml_declaration=True)



for item in os.listdir(INPUT):
	df=pd.read_csv(INPUT+item, index_col=0)
	name=item.split(".")[0]
	generateMatrix(PATH+name, df)