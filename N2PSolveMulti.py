import os
import re
import sys
import subprocess
import multiprocessing




if(len(sys.argv))>=3:
	INPUT=sys.argv[1]+"/"
	OUTPUT=sys.argv[2]+"/"
else:
	print ("USAGE: {} INPUT OUTPUT [THREADS] [CONFIG_FILE] [DEBUG]".format(sys.argv[0]))
	sys.exit()
if(len(sys.argv)>=4):
	K=int(sys.argv[3])
else:
	K=10

if(len(sys.argv)>=5):
	FILE=sys.argv[4]
else:
	FILE="solve.cfg"

if(len(sys.argv)==6):
	DEBUG=True
else:
	DEBUG=False

N2P_PATH="../Net2Plan/"
ALGO="Offline_ipOverWdm_routingSpectrumAndModulationAssignmentILPNotGrooming"
ALGO_PATH="../Net2Plan/workspace/builtInExamples.jar"
PARAMS=[]
with open(FILE, "r") as f:
	for i,line in enumerate(f):
		if(i==0):
			N2P_PATH=re.sub("[\n\r]", "", line)
		if(i==1):
			ALGO_PATH=re.sub("[\n\r]", "", line)
		if(i==2):
			ALGO=re.sub("[\n\r]", "", line)
		if(i>2):
			PARAMS.append(re.sub("[\n\r]", "", line))

def callN2P(FILES):
	global N2P_PATH
	global ALGO
	global ALGO_PATH
	global PARAMS
	FI=FILES[0]
	FO=FILES[1]
	devnull = open(os.devnull, 'w')
	system_call="java -jar {}/Net2Plan-CLI.jar --mode net-design --input-file {} --output-file {} --class-file {} --class-name {} --alg-param solverName=cplex ".format(N2P_PATH, FI, FO, ALGO_PATH, ALGO)
	params=" ".join(["--alg-param {}".format(x) for x in PARAMS])
	if DEBUG:
				subprocess.call(system_call+params, shell=True) 
	else:
		subprocess.call(system_call+params, shell=True, stdout=devnull, stderr=devnull) 


print("Starting program")

all_files=[("./"+INPUT+f, "./"+OUTPUT+f) for f in os.listdir(INPUT)]
pool=multiprocessing.Pool(K)

pool.map(callN2P, all_files)

print("Program Finished!")