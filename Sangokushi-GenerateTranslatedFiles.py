#!/usr/bin/python2.7 by kuronosuFear
from __future__ import print_function
import os
import struct
import sys
import binascii

reload(sys)
sys.setdefaultencoding('utf-8')
path = 'Sangokushi-Translated\\'

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def type1recompile():
	with open('Sangokushi-script-Type1.tsv', 'rb') as fo:
		tempData = fo.readlines()
	choppedText=[]
	for line in range(len(tempData)):
		choppedText+=(tempData[line].rstrip('\n')).split('\t')
	choppedText = chunks(choppedText, 8)
	x=1 #skip header index
	EndIndex=1 #skip header index
	z=0
	allStrings = [] 
	while(x<len(choppedText)-1):
		for x in range(EndIndex, len(choppedText)):
			filename = choppedText[x][0]
			if(filename=='END'):
				break
			tempy = (choppedText[x][6]+b'\x00').replace('\\n', b'\x0a')
			tempy = tempy.replace('NULL', b'\x00')
			tempy = tempy.replace('\x27', '\xc2\xb4') #replace apostrophe with accute accent
			tempy = tempy.replace('...', '\xe2\x80\xa6') #replace triple-dots with ellipses
			tempy = tempy.replace('"', '\xe2\x80\xb3') #replace doublequotes with double prime
			tempy = tempy.replace('\x00\x00', b'\x00')
			allStrings.append(tempy)
			z+=1
			if(choppedText[x+1][0] != filename):
				EndIndex += z
				break
		z=0
		if(filename=='END'):
			break
		fileTable = struct.pack("<I", len(allStrings))
		fileData = ''
		dataOffset = (len(allStrings)*4*2)+4
		#print(int(dataOffset))
		for y in range(0, len(allStrings)):
			fileTable += struct.pack("<I", dataOffset) + struct.pack("<I", len(allStrings[y]))
			dataOffset+=len(allStrings[y])
			fileData += allStrings[y]
		fileTable+=fileData
		with open(path+filename, 'wb') as fo:
			fo.write(fileTable) #erase contents
		print('Generated: ' + filename + '             ', end='\r') 
		allStrings = []
		x+=1
	print('\nType1 files done...')
	return


def type3recompile():
	with open('Sangokushi-script-Type3.tsv', 'rb') as fo:
		tempData = fo.readlines()
	choppedText=[]
	for line in range(len(tempData)):
		choppedText+=(tempData[line].rstrip('\n')).split('\t')
	choppedText = chunks(choppedText, 8)
	x=1 #skip header index
	EndIndex=1 #skip header index
	z=0
	allStrings = [] 
	while(x<len(choppedText)-1):
		for x in range(EndIndex, len(choppedText)):
			filename = choppedText[x][0]
			if(filename=='END'):
				break
			tempy = (choppedText[x][6][18:]+b'\x00').replace('\\n', b'\x0a')
			tempy = tempy.replace('NULL', b'\x00')
			tempy = tempy.replace('\x27', '\xc2\xb4') #replace apostrophe with accute accent
			tempy = tempy.replace('...', '\xe2\x80\xa6') #replace triple-dots with ellipses
			tempy = tempy.replace('"', '\xe2\x80\xb3') #replace doublequotes with double prime
			tempy = tempy.replace('\x00\x00', b'\x00')
			allStrings.append((binascii.unhexlify(choppedText[x][6][1:17])+tempy))
			z+=1
			if(choppedText[x+1][0] != filename):
				EndIndex += z
				break
		z=0
		if(filename=='END'):
			break
		fileTable = b'\x62\x29\x00\x00' + struct.pack("<I", len(allStrings))
		fileData = ''
		dataOffset = (len(allStrings)*4)+8
		for y in range(0, len(allStrings)):
			fileTable += struct.pack("<I", dataOffset)
			dataOffset+=len(allStrings[y])
			fileData += allStrings[y]
		fileTable+=fileData
		with open(path+filename, 'wb') as fo:
			fo.write(fileTable) #erase contents
		print('Generated: ' + filename + '             ', end='\r') 
		allStrings = []
		x+=1
	print('\nType3 files done...')
	return

def type4recompile():
	with open('Sangokushi-script-Type4.tsv', 'rb') as fo:
		tempData = fo.readlines()
	choppedText=[]
	for line in range(len(tempData)):
		choppedText+=(tempData[line].rstrip('\n')).split('\t')
	choppedText = chunks(choppedText, 8)
	x=1 #skip header index
	EndIndex=1 #skip header index
	z=0
	allStrings = []
	entryOneLength = 0
	while(x<len(choppedText)-1):
		for x in range(EndIndex, len(choppedText)):
			filename = choppedText[x][0]
			if(filename=='END'):
				break
			tempy = (choppedText[x][6]+b'\x00').replace('\\n', b'\x0a')
			tempy = tempy.replace('NULL', b'\x00')
			tempy = tempy.replace('\x27', '\xc2\xb4') #replace apostrophe with accute accent
			tempy = tempy.replace('...', '\xe2\x80\xa6') #replace triple-dots with ellipses
			tempy = tempy.replace('"', '\xe2\x80\xb3') #replace doublequotes with double prime
			tempy = tempy.replace('\x00\x00', b'\x00')
			entryOneLength+=len(tempy)
			allStrings.append(tempy)
			z+=1
			if(choppedText[x+1][0] != filename  or choppedText[x][3]=='1'):
				EndIndex += z
				break
		z=0
		if(filename=='END'):
			break
		entryTwo = (choppedText[x][6]).split(';')
		entryTwoData = binascii.unhexlify(entryTwo[1])
		fileTable = b'\x02\x00\x00\x00\x14\x00\x00\x00' + struct.pack("<I",((len(allStrings)-1)*4*2)+4+entryOneLength-len(choppedText[x][6])-1) + struct.pack("<I",((len(allStrings)-1)*4*2)+4+entryOneLength-len(choppedText[x][6])-1 + 20) + struct.pack("<I", len(entryTwoData)) + struct.pack("<I", len(allStrings)-1)
		fileData = ''
		dataOffset = (len(allStrings)*4*2)-4
		#print(int(dataOffset))
		for y in range(0, len(allStrings)-1):
			fileTable += struct.pack("<I", dataOffset) + struct.pack("<I", len(allStrings[y]))
			dataOffset+=len(allStrings[y])
			fileData += allStrings[y]
		fileTable+=fileData+entryTwoData
		with open(path+filename, 'wb') as fo:
			fo.write(fileTable) #erase contents
		print('Generated: ' + filename + '             ', end='\r') 
		allStrings = []
		entryOneLength = 0
		x+=1
	print('\nType4 files done...')
	return

def type2recompile():
	with open('Sangokushi-script-Type2.tsv', 'rb') as fo:
		tempData = fo.readlines()
	choppedText=[]
	for line in range(len(tempData)):
		choppedText+=(tempData[line].rstrip('\n')).split('\t')
	choppedText = chunks(choppedText, 8)
	x=1 #skip header index
	StartIndex=1 #skip header index
	EndIndex=1 #skip header index
	z=0
	allStrings = []
	entryCounter=0
	l=0 #linecounter
	lineCounterList = []
	entryStringLength = 0
	entryStringLengthList = []
	while(x<len(choppedText)-1):
		for x in range(EndIndex, len(choppedText)):
			filename = choppedText[x][0]
			if(choppedText[x][3]=='0' and choppedText[x][4]=='0'):
				StartIndex=x
			if(filename=='END'):
				break
			if(choppedText[x][3]!=choppedText[x+1][3]):
				entryCounter+=1
			tempy = (choppedText[x][6]+b'\x00').replace('\\n', b'\x0a')
			tempy = tempy.replace('NULL', b'\x00')
			tempy = tempy.replace('\x27', '\xc2\xb4') #replace apostrophe with accute accent
			tempy = tempy.replace('...', '\xe2\x80\xa6') #replace triple-dots with ellipses
			tempy = tempy.replace('"', '\xe2\x80\xb3') #replace doublequotes with double prime
			tempy = tempy.replace('\x00\x00', b'\x00')
			entryStringLength+=len(tempy)
			allStrings.append(tempy)
			l+=1
			z+=1
			if(choppedText[x+1][4]=='0' or choppedText[x+1][4]=='END'):
				lineCounterList.append(l)
				entryStringLengthList.append(entryStringLength)
				entryStringLength = 0
				l=0
			if(choppedText[x+1][0] != filename):
				EndIndex += z - 1
				break
		z=0
		if(filename=='END'):
			break
		if(entryCounter == 0):
			entryCounter =1
		fileTable = struct.pack("<I", entryCounter)
		currentOffset = 4
		f = 0
		for f in range(entryCounter):
			fileTable += struct.pack("<I", entryCounter*8+currentOffset) + struct.pack("<I", (lineCounterList[f]*8+4)+entryStringLengthList[f])
			currentOffset +=(lineCounterList[f]*8+4)+entryStringLengthList[f]
		f = 0
		fileData = ''
		iterString = 0
		limitless=0
		for f in range(entryCounter):
			fileTable += struct.pack("<I", lineCounterList[f])
			currentOffset = 4
			lt=0
			for lt in range(lineCounterList[f]):
				fileTable += struct.pack("<I", lineCounterList[f]*8+currentOffset) + struct.pack("<I", len(allStrings[limitless]))
				currentOffset += len(allStrings[limitless])
				fileData += allStrings[limitless]
				limitless+=1
			fileTable += fileData
			fileData = ''
		with open(path+filename, 'wb') as fo:
			fo.write(fileTable) #erase contents
		print('Generated: ' + filename + '             ', end='\r') 
		allStrings = []
		lineCounterList = []
		entryStringLength = 0
		entryStringLengthList = []
		EndIndex+=1
		x+=1
		entryCounter=0
	print('\nType2 files done...')
	return

if not os.path.exists(os.path.dirname(path)):
	try:
		os.makedirs(os.path.dirname(path))
	except OSError as exc: # Guard against race condition
		if exc.errno != errno.EEXIST:
			raise

type1recompile()
type2recompile()
type3recompile()
type4recompile()