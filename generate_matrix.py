import sys
import time
import random
import numpy as np
import multiprocessing
import xml.etree.ElementTree as ET

supported_modes=["GAUSSIAN", "UNIFORM"]

if(len(sys.argv))>=4:
	NUM_MATRICES=int(sys.argv[1])
	PATH=sys.argv[2]+"/"
	CANONICAL=sys.argv[3]
else:
	print ("USAGE: {} NUM_MATRICES PATH_OUT CANONICAL_FILE [VARIABILITY] [MULTIPLICITY_FACTOR] [MODE] [THREAD_POOL] \n Supported modes: {}".format(sys.argv[0], supported_modes))
	sys.exit()


if(len(sys.argv)>=5):
	VARIABILITY=float(sys.argv[4])
else:
	VARIABILITY=0.1

if(len(sys.argv)>=6):
	MULTIPLICITY=float(sys.argv[5])
else:
	MULTIPLICITY=1

if(len(sys.argv)>=7):
	MODE=sys.argv[6]
else:
	MODE="GAUSSIAN"

if(len(sys.argv)>=8):
	K=int(sys.argv[7])
else:
	K=5


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
					item.set("offeredTraffic", str(trunc(ModifyRandomly( MODE,float(item.get("offeredTraffic"))*MULTIPLICITY, VARIABILITY*MULTIPLICITY))))

	e.write(fout, xml_declaration=True)


print("[{}] Starting program".format(time.strftime("%d/%m/%Y - %H:%M:%S")))

all_files=[PATH+str(i)+".n2p" for i in range(NUM_MATRICES)]

pool=multiprocessing.Pool(K)

results=pool.map(generateMatrix, all_files)

print("[{}] Program Finished!".format(time.strftime("%d/%m/%Y - %H:%M:%S")))