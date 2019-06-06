import sys
import xlrd
from xlutils.copy import copy
import statistics

def main():
	line = int(sys.argv[3]) + 1
	folder = ""
	if(sys.argv[1] == "MaxMin"):
		folder = "resultsMaxMin/PFSP_instances/"
		fileName = folder + sys.argv[2]
	elif(sys.argv[1] == "ACS"):
		folder = "resultsACS/PFSP_instances/"
		fileName = folder + sys.argv[2]
	
	xlsFile = folder +"All.xls"
	workbook = xlrd.open_workbook(xlsFile)
	workbook = copy(workbook)
	worksheet = workbook.get_sheet(0)
	
	#To DO
	column = 0
	f = open(fileName, "r")
	f1 = f.readlines()
	maxVal = None
	minVal = 0
	meanVal = 0
	std = 0
	values = []
	for elem in f1:
		if(column > 0):
			worksheet.write(line, column,int(elem))
			values.append(int(elem))
		column += 1
	worksheet.write(line,column, min(values))
	worksheet.write(line,column+1, max(values))
	worksheet.write(line,column+2, statistics.mean(values))
	worksheet.write(line,column+3, statistics.stdev(values))

	workbook.save(xlsFile)
	f.close()



if __name__ == "__main__":
    main()