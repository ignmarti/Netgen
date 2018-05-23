import sys
import random
import numpy as np
import multiprocessing
import xml.etree.ElementTree as ET

supported_modes=["GAUSSIAN", "UNIFORM"]

if(len(sys.argv))>=3:
	NUM_MATRICES=int(sys.argv[1])
	PATH=sys.argv[2]+"/"
else:
	print ("USAGE: {} NUM_MATRICES PATH_OUT [VARIABILITY] [THREAD_POOL] [CANONICAL_FILE] [MULTIPLICITY_FACTOR] [MODE]\n Supported modes: {}".format(sys.argv[0], supported_modes))
	sys.exit()


if(len(sys.argv)>=4):
	VARIABILITY=float(sys.argv[3])
else:
	VARIABILITY=0.1

if(len(sys.argv)>=5):
	K=int(sys.argv[4])
else:
	K=10

if(len(sys.argv)>=6):
	CANONICAL=sys.argv[5]
else:
	CANONICAL="canonical.n2p"

if(len(sys.argv)>=7):
	MULTIPLICITY=float(sys.argv[6])
else:
	MULTIPLICITY=1

if(len(sys.argv)>=8):
	MODE=sys.argv[7]
else:
	MODE="GAUSSIAN"


def generateRandomNumbers(center):
	return(random.random()*center)
def generateGaussianNumbers(mean, variability=0.1):
	return(np.random.normal(mean, variability))

def ModifyRandomly(mode, mean, variability):
	if(mode==supported_modes[0]):
		return(generateGaussianNumbers(mean, variability))
	elif(mode==supported_modes[1]):
		return(generateRandomNumbers(mean))

def trunc(integer):
	if(integer>0):
		return (integer)
	else:
		return(0.00000000001)

def generateMatrix(fout):
	global CANONICAL
	np.random.seed()
	e = ET.parse(CANONICAL)
	root=e.getroot()
	for child in root:
		if child.tag=="layer":
			for item in child:
				if item.tag=="demand":
					item.set("offeredTraffic", str(trunc(ModifyRandomly( MODE,float(item.get("offeredTraffic"))*MULTIPLICITY, VARIABILITY*MULTIPLICITY*float(item.get("offeredTraffic"))))))

	e.write(fout, xml_declaration=True)

all_files=[PATH+str(i)+".n2p" for i in range(NUM_MATRICES)]

pool=multiprocessing.Pool(K)

results=pool.map(generateMatrix, all_files)