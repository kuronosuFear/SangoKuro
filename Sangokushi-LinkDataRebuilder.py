#!/usr/bin/python2.7 by kuronosuFear
from __future__ import print_function
import os
import struct
import zlib 

def pad(s):
    return s + b"\x00" * (32 - len(s) % 32)
    
def compressData(data,rawsize):
	address=0
	remainingSize=rawsize
	defaultSize=32768
	compressed = struct.pack("<I", rawsize)
	temp=''
	while(1):
		compressor = zlib.compressobj(9, zlib.DEFLATED, +15, 9, 0)
		if(remainingSize<defaultSize):
			defaultSize=remainingSize
		temp = compressor.compress(data[address:address+defaultSize])
		temp = compressor.flush()
		compressed+= struct.pack("<I", len(temp)+2) + b'\x78\xda' + temp
		remainingSize-=defaultSize
		address+=defaultSize
		#print(str(address) + ' ' + str(defaultSize) + ' ' + str(remainingSize))
		if (address==rawsize or remainingSize==0 or defaultSize==0):
			break
	return compressed

path = 'Sangokushi-Xtracted\\'

Header = b'\x1D\x78\x33\x01\xDD\x4A\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00'
StartFileOffset = (19165 * 16) + 16
#StartFileOffset = (1 * 16) + 16
EntryAddress = StartFileOffset
ShortAddress = EntryAddress/32
Reserved = struct.pack("<I", 0) #Null DWORD
Table = Header

with open('LINKDATA-Body', 'wb') as fo:
	fo.write('') #erase contents

print ('Compressing compressable files')
counter = 0 #for confirmation
for subdir, dirs, files in os.walk(path):
    for file in files:
    	intIndex = int((os.path.splitext(file)[0])[0:8]) #index
    	marker = (os.path.splitext(file)[0])[9]
    	intSize = os.path.getsize(os.path.join(subdir,file))
    	#if (intSize%32 != 0):
    		#intSize = intSize + (32 - (intSize%32)) # align size, thus aligning EntryAddress
    	ShortAddress = EntryAddress/32
    	with open(os.path.abspath(os.path.join(subdir,file)), 'rb') as fo:
    		tempData = fo.read()
    	if (counter != intIndex):
    		print ('Error encountered in Index#'+ str(intIndex))
    		break
    	if(marker=='U'):
    		counter+=1
    		if (len(tempData)%32 != 0):
    			tempData = pad(tempData)
    		EntryAddress += len(tempData)
    		Table += struct.pack("<I", ShortAddress) + Reserved + struct.pack("<I", intSize) + Reserved
    		with open('LINKDATA-Body', 'ab') as fo:
    			fo.write(tempData)
    		tempData=''
    		print(str(intIndex+1) + ' of 19165 files done... Size: ' + str(intSize) + '             ', end='\r')
    		continue
    	tempData = compressData(tempData,intSize)
    	#if (len(tempData)%32 != 0):
    	tempData = pad(tempData)
    	if (len(tempData)%32 ==0):
    		tempData = tempData + b"\x00" * (32)
    	EntryAddress += len(tempData)
    	Table += struct.pack("<I", ShortAddress) + Reserved + struct.pack("<I", len(tempData)) + struct.pack("<I", intSize)
    	with open('LINKDATA-Body', 'ab') as fo:
    		fo.write(tempData)
    	tempData=''
    	counter+=1
    	print(str(intIndex+1) + ' of 19165 files done... Size: ' + str(intSize) + '             ', end='\r')
    	#if (intIndex>=2):
    		#break

with open('LINKDATA-Table', 'wb') as fo:
	fo.write(Table)
	
with open('LINKDATA-Body', 'rb') as fb:
	body = fb.read()
	
with open('LINKDATA_A.BIN-new', 'wb') as f:
	f.write(Table + body)
	
with open('LINKDATA-Table', 'wb') as fo:
	fo.write('')
	
with open('LINKDATA-Body', 'wb') as fb:
	fb.write('')

#print ('Building File Table...')
##Building initial table
#for subdir, dirs, files in os.walk(path):
#    for file in files:
#        ext = (os.path.splitext(file)[0])[0:8]
#        intIndex  = int(ext) 
#        intSize = os.path.getsize(os.path.join(subdir,file))
#        if (intSize%32 != 0):
#        	intSize = intSize + (32 - (intSize%32)) # align size, thus aligning EntryAddress
#        #print str(intIndex) + " " +str(EntryAddress)
#        ShortAddress = EntryAddress/32
#        EntryAddress += intSize
#        LinkData += struct.pack("<I", ShortAddress) + Reserved + struct.pack("<I", intSize) + Reserved
#
#print ('File Table has been built...')
#print ('Adding data for the files...')
#
#with open('LINKDATA_A.BIN-2', 'wb') as fo:
#	fo.write(LinkData)
#
#counter = 0 #for confirmation
#for subdir, dirs, files in os.walk(path):
#    for file in files:
#        ext = (os.path.splitext(file)[0])[0:8]
#        intIndex  = int(ext)
#        if (counter != intIndex):
#        	continue
#        with open(os.path.abspath(os.path.join(subdir,file)), 'rb') as fo:
#        	tempData = fo.read()
#        intSize = os.path.getsize(os.path.join(subdir,file))
#        
#        if (intSize%32 != 0):
#        	tempData = pad(tempData)
#        with open('LINKDATA_A.BIN-2', 'ab') as fo:
#        	fo.write(tempData)
#        print(str(intIndex+1) + ' of 19165 files done... Size: ' + str(intSize), end='\r')
#        tempData='' #purge from memory
#        counter += 1