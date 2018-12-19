#!/usr/bin/python2.7 by kuronosuFear
from __future__ import print_function
import os
import struct
import numpy as np
import sys
import binascii

reload(sys)
sys.setdefaultencoding('utf-8')

path = 'Sangokushi-Xtracted\\'
export = 'Sangokushi-script.csv'
type3header = b'\x62\x92\x00\x00'
csvheader = 'Filename\tIndex\tType\tEntry#\tLine#\tOriginal Text\tTranslated Text\tRemarks\n'

with open('Sangokushi-script-Type1.tsv', 'wb') as fo:
	fo.write(csvheader)

with open('Sangokushi-script-Type2.tsv', 'wb') as fo:
	fo.write(csvheader)
	
with open('Sangokushi-script-Type3.tsv', 'wb') as fo:
	fo.write(csvheader)
	
with open('Sangokushi-script-Type4.tsv', 'wb') as fo:
	fo.write(csvheader)

def dword2int(dword):
	#dword = int(dword.encode('hex'),16)
	return int(np.fromstring(dword, dtype=int))

def type2extraction(filepath, name, entrynum):
	with open(filepath, 'rb') as fo:
		tempData = fo.read()
	numberOfEntries = dword2int(tempData[0:4])
	entryTable = np.memmap(filepath, dtype=int, offset=4, mode='r', shape=(numberOfEntries,2)) # entryOffset, entrySize
	for x in range(numberOfEntries):
		if (entryTable[x][1] == 0 or entryTable[x][1]>=len(tempData)):
			continue
		numberOfLines = dword2int(tempData[entryTable[x][0]:entryTable[x][0]+4])
		if(numberOfLines == 0):
			with open('Sangokushi-script-Type2.tsv', 'ab') as fo:
				fo.write(name +'\t'+ str(entrynum)+ '\t2\t'+str(x)+'\t' + str(y) + '\t' + 'NULL' + '\t\t\n')
			continue
		if(numberOfLines*8>entryTable[x][1]):
			#print ('invalid entry') # might corrupt if the game checks this corrupted value once recompiled
			continue
		tableData = np.memmap(filepath, dtype=int, offset=entryTable[x][0]+4, mode='r', shape=(numberOfLines,2)) #lineOffset, stringLength
		for y in range(numberOfLines): 
			origText = tempData[(entryTable[x][0]+tableData[y][0]):(entryTable[x][0]+tableData[y][0]+tableData[y][1]-1)]
			origText =  origText.replace(b'\x0a', '\\n')
			if(tableData[y][1]==1):
				origText='NULL'
			with open('Sangokushi-script-Type2.tsv', 'ab') as fo:
				fo.write(name +'\t'+ str(entrynum)+ '\t2\t'+str(x)+'\t' + str(y) + '\t' + origText + '\t' + origText + '\t\n')
		y=0
		tableData=''
	return

def type1extraction(filepath, name, entrynum):
	with open(filepath, 'rb') as fo:
		tempData = fo.read()
	numberOfLines = dword2int(tempData[0:4])
	tableData = np.memmap(filepath, dtype=int, offset=4, mode='r', shape=(numberOfLines,2))     
	for x in range(numberOfLines):
		origText = tempData[tableData[x][0]:tableData[x][0]+tableData[x][1]-1]
		origText =  origText.replace(b'\x0a', '\\n')
		with open('Sangokushi-script-Type1.tsv', 'ab') as fo:
			fo.write(name +'\t'+ str(entrynum)+ '\t1\t0\t' + str(x) + '\t' + origText + '\t' + origText + '\t\n')
	return
	
def type3extraction(filepath, name, entrynum):
	with open(filepath, 'rb') as fo:
		tempData = fo.read()
	if(len(tempData)<=16):
		return
	numberOfLines = dword2int(tempData[4:8])
	tempTable = np.memmap(filepath, dtype=int, offset=8, mode='r', shape=(numberOfLines+1,1))
	tableData = tempTable.copy() #make it writeable
	tempTable = ''#obliterate tempTable to prevent memleaks
	tableData.setflags(write=1)
	tableData[numberOfLines] = len(tempData)
	for x in range(numberOfLines):
		origText = tempData[tableData[x][0]:((tableData[x+1][0]))]
		eightBytes = '<' + binascii.hexlify(origText[0:8]) +'>'
		origText = origText.replace(origText[0:8], eightBytes)
		origText = origText.replace(b'\x0a', '\\n')
		origText = origText[:origText.find(b'\x00')] #remove trailing data
		with open('Sangokushi-script-Type3.tsv', 'ab') as fo:
			fo.write(name +'\t'+ str(entrynum)+ '\t3\t0\t' + str(x) + '\t' + origText + '\t' + origText + '\t\n')
	return

def type4extraction(filepath, name, entrynum):
	with open(filepath, 'rb') as fo:
		tempData = fo.read()
	numberOfEntries = dword2int(tempData[0:4])
	entryTable = np.memmap(filepath, dtype=int, offset=4, mode='r', shape=(2,2)) # entryOffset, entrySize
	x=0
	numberOfLines = dword2int(tempData[entryTable[x][0]:entryTable[x][0]+4])
	if(numberOfLines == 0):
		with open(export, 'ab') as fo:
			fo.write(name +'\t'+ str(entrynum)+ '\t2\t'+str(x)+'\t' + str(y) + '\t' + 'NULL' + '\t\t\n')
	tableData = np.memmap(filepath, dtype=int, offset=entryTable[x][0]+4, mode='r', shape=(numberOfLines,2)) #lineOffset, stringLength
	for y in range(numberOfLines): 
		origText = tempData[(entryTable[x][0]+tableData[y][0]):(entryTable[x][0]+tableData[y][0]+tableData[y][1]-1)]
		origText =  origText.replace(b'\x0a', '\\n')
		if(tableData[y][1]==1):
			origText='NULL'
		with open('Sangokushi-script-Type4.tsv', 'ab') as fo:
			fo.write(name +'\t'+ str(entrynum)+ '\t4\t0\t' + str(y) + '\t' + origText + '\t' + origText + '\t\n')
	tableData=''
	with open('Sangokushi-script-Type4.tsv', 'ab') as fo:
		fo.write(name +'\t'+ str(entrynum)+ '\t4\t1\t0\t' + str(entryTable[1][1])+';'+ binascii.hexlify(tempData[entryTable[1][0]:(entryTable[1][0]+entryTable[1][1])]) + '\t\t\n')
	entryTable=''
	return

for subdir, dirs, files in os.walk(path):
	for file in files:
		ext = os.path.splitext(file)[-1].lower()
		entrynum = int((os.path.splitext(file)[0])[0:8]) #index
		if ext == '.script':
			print(file + '             ')#, end='\r')
			if(entrynum>=53 and entrynum<=59 and entrynum!=54):
				type2extraction(os.path.abspath(os.path.join(subdir,file)), file, entrynum)
			if(entrynum>=13585 and entrynum<=14264):
				type1extraction(os.path.abspath(os.path.join(subdir,file)), file, entrynum)
			if (entrynum>=16112 and entrynum<=16131):
				type3extraction(os.path.abspath(os.path.join(subdir,file)), file, entrynum)
			if((entrynum>=15134 and entrynum<=15954) or (entrynum>=61 and entrynum<=63)):
				type4extraction(os.path.abspath(os.path.join(subdir,file)), file, entrynum)


with open('Sangokushi-script-Type1.tsv', 'ab') as fo:
	fo.write('END\tEND\tEND\tEND\tEND\tEND\tEND\tEND')

with open('Sangokushi-script-Type2.tsv', 'ab') as fo:
	fo.write('END\tEND\tEND\tEND\tEND\tEND\tEND\tEND')
	
with open('Sangokushi-script-Type3.tsv', 'ab') as fo:
	fo.write('END\tEND\tEND\tEND\tEND\tEND\tEND\tEND')
	
with open('Sangokushi-script-Type4.tsv', 'ab') as fo:
	fo.write('END\tEND\tEND\tEND\tEND\tEND\tEND\tEND')