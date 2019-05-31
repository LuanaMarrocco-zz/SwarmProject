import sys

fileName = "PFSP_instances/DD_Ta051.txt"
M = 0
N = 0
processingTime = [] #N lines, M colums
dueDates = []
weights = []
alpha=1.0
beta=1.0
rho=0.2
n_ants=10
max_iterations=0
max_tours=10000
seed = 0

def readFile():
	global M,N, processesTime, dueDates, weights, fileName
	f=open(fileName, "r")
	lines = f.readlines()
	i = 0
	for line in lines:
		if(i == 0):
			N,M = list(map(int, line.split()))
			i = i+1
		elif(i <= N):
			processingTime.append(list(map(int, line.split())))
			i += 1
		else:
			content = line.split()
			if(content[0] != "Reldue"):
				_,date,_,weight = list(map(int, content))
				dueDates.append(date)
				weights.append(weight)


def readArguments():
	global n_ants,alpha,beta,rho, max_iterations, max_tours, seed, fileName
	i = 1
	retVal = True
	while(i < len(sys.argv)):
		if(sys.argv[i] == "--ants"):
			n_ants = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--alpha"):
			alpha = int(sys.argv[i+1])
			i += 1
		elif(sys.argv[i] == "--beta"):
			beta = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--rho"):
			rho = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--iterations"):
			max_iterations = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--tours"):
			max_tours = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--seed"):
			seed = sys.argv[i+1]
			i += 1
		elif(sys.argv[i] == "--instance"):
			fileName = sys.argv[i+1]
			i += 1
		else:
			print("Parameter ", sys.argv[i], " not recognized")
			retVal = False
		i += 1
	return retVal




def main() :
	if(readArguments()):
		readFile()

if __name__ == "__main__":
    main()

