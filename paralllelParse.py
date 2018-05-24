import os
import re
import sys
import csv
import multiprocessing
import xml.etree.ElementTree as ET

supported_modes=["IPWDM", "FORMU", "11PATH"]

if(len(sys.argv))>=3:
	INPUT=sys.argv[1]+"/"
	OUTPUT=sys.argv[2]
else:
	if(len(sys.argv)==2):
		if(sys.argv[1].lower()=="mode"):
			print("    SUPPORTED MODEs: {}".format(",".join(supported_modes)))
		else:
			print ("USAGE: {} INPUT OUTPUT [MODE] [THREADS]".format(sys.argv[0]))
			print("    SUPPORTED MODEs: {}".format(",".join(supported_modes)))
	else:
		print ("USAGE: {} INPUT OUTPUT [MODE] [THREADS]".format(sys.argv[0]))
		print("    SUPPORTED MODEs: {}".format(",".join(supported_modes)))
	sys.exit()

if(len(sys.argv)>=4):
	MODE=sys.argv[3]
else:
	MODE="IPWDM"
if (len(sys.argv)==5):
	K=int(sys.argv[4])
else:
	K=10



def parseN2PIPWDM(fin):
	e = ET.parse(fin)
	root=e.getroot()
	result_IP={}
	result_WDM={}
	label_ids={}
	for child in root:
		if child.tag=="layer" and child.get("name")=="IP":
			label_ids={}
			for c in child:
				if(c.tag=="link"):
					label="{}-{}".format(c.get("originNodeId"), c.get("destinationNodeId"))
					value=c.get("capacity")
					result_IP[label+"_l"]=value
					label_ids[c.get("id")]=label
				if(c.tag=="demand"):
					label="{}:{}-{}".format(c.get("id"),c.get("egressNodeId"), c.get("ingressNodeId"))
					value=c.get("offeredTraffic")
					result_IP[label+"_d"]=value
					label_ids[c.get("id")]=label

				if c.tag=="sourceRouting":
					prev=""
					count=1
					for r in c:
						demandId= r.get("demandId")
						label=label_ids.get(demandId)
						if(prev==label):
							count+=1
						else:
							count=1
							prev=label
						traffic= r.get("currentCarriedTrafficIfNotFailing")
						label="{}:{}".format(str(count),label)
						result_IP[label+"_t"]=traffic
		if child.tag=="layer" and child.get("id")=="1":
			label_ids={}
			prev=""
			count=1
			for c in child:
				if(c.tag=="demand"):
					label="{}-{}".format(c.get("egressNodeId"), c.get("ingressNodeId"))
					if(prev==label):
						count+=1
					else:
						count=1
						prev=label
					value=c.get("offeredTraffic")
					label="{}:{}".format(str(count),label)
					result_WDM[label+"_d"]=value
					label_ids[c.get("id")]=label
					
			for c in child:
				if(c.tag=="link"):
					label="{}-{}".format(c.get("originNodeId"), c.get("destinationNodeId"))
					value=c.get("capacity")
					result_WDM[label+"_l"]=value
				if c.tag=="sourceRouting":
					for r in c:
						demandId= r.get("demandId")
						label=label_ids.get(demandId)
						for a in r:
							if a.get("key")=="seqFrequencySlots_se":
								fs=re.sub("^\s", "", a.get("value")).split(" ")
								lambdas=":-:".join(fs)
								result_WDM[label+"_s"]=lambdas
						lnks=r.get("currentPath").split(" ")
						FS=fs[0]
						hops=":-:".join(lnks)
						wdms=":-:".join([x+";"+FS for x in lnks])
						result_WDM[label+"_h"]=hops
						result_WDM[label+"_a"]=wdms
				
	return([result_IP, result_WDM])

def parseN2PFormulations(fin):
	e = ET.parse(fin)
	root=e.getroot()
	result={}
	label_ids={}
	for child in root:
		if child.tag=="layer" and child.get("id")=="1":
			for c in child:
				if(c.tag=="demand"):
					label="{}-{}".format(c.get("egressNodeId"), c.get("ingressNodeId"))
					value=c.get("offeredTraffic")
					result[label+"_d"]=value
					label_ids[c.get("id")]=label
				if c.tag=="sourceRouting":
					for r in c:
						demandId= r.get("demandId")
						label=label_ids.get(demandId)
						traffic= r.get("currentCarriedTrafficIfNotFailing")
						hops=":-:".join(r.get("currentPath").split(" "))
						result[label+"_t"]=traffic
						result[label+"_h"]=hops
				if(c.tag=="link"):
					label="{}:{}-{}".format(c.get("id"),c.get("originNodeId"), c.get("destinationNodeId"))
					value=c.get("capacity")
					result[label+"_l"]=value
	return(result)

def parseN2P11Path(fin):
	e = ET.parse(fin)
	root=e.getroot()
	result={}
	label_ids={}
	for child in root:
		if child.tag=="layer" and child.get("id")=="1":
			for c in child:
				if(c.tag=="demand"):
					label="{}-{}".format(c.get("egressNodeId"), c.get("ingressNodeId"))
					value=c.get("offeredTraffic")
					result[label+"_d"]=value
					label_ids[c.get("id")]=label
				if c.tag=="sourceRouting":
					for r in c:
						demandId= r.get("demandId")
						label=label_ids.get(demandId)
						traffic= r.get("currentCarriedTrafficIfNotFailing")
						hops=":-:".join(r.get("currentPath").split(" "))
						if(r.get("backupRoutes")==""):
							result[label+"_t"]=traffic
							result[label+"_h"]=hops
						else:
							result[label+"_tb"]=traffic
							result[label+"_hb"]=hops

	return(result)

print("Starting program")

all_files=[INPUT+ x for x in os.listdir(INPUT)]
print("There are {} files to parse".format(len(all_files)))

pool=multiprocessing.Pool(K)

if(MODE==supported_modes[1]):
	results=pool.map(parseN2PFormulations, all_files)
elif(MODE==supported_modes[2]):
	results=pool.map(parseN2P11Path, all_files)
else:
	result_ip=[]
	result_wdm=[]
	results=pool.map(parseN2PIPWDM, all_files)
	for result in results:
		result_ip.append(result[0])
		result_wdm.append(result[1])
	with open(OUTPUT+"_IP.csv", 'w') as csvfile:
		fieldnames=[]
		for elems in result_ip:
			fieldnames.extend(elems.keys())
		fieldnames=list(set(fieldnames))
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in result_ip:
			writer.writerow(item)
	with open(OUTPUT+"_WDM.csv", 'w') as csvfile:
		fieldnames=[]
		for elems in result_wdm:
			fieldnames.extend(elems.keys())
		fieldnames=list(set(fieldnames))
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in result_wdm:
			writer.writerow(item)
	print("Program Finished! Items stored in: {}_IP.csv and {}_WDM.csv".format(OUTPUT, OUTPUT))
	exit()

if OUTPUT[-3:]!=".csv":
	OUTPUT=OUTPUT+".csv"
	
with open(OUTPUT, 'w') as csvfile:
	fieldnames=[]
	for elems in results:
		fieldnames.extend(elems.keys())
	fieldnames=list(set(fieldnames))

	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for item in results:
		writer.writerow(item)

print("Program Finished! {} Items stored in: {}".format(len(all_files), OUTPUT))