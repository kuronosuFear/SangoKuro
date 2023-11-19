
import io
import zlib
import numpy as np
import os

allowedChars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-_ ')

def dword2int(dword):
    return int.from_bytes(dword, byteorder='little', signed=False)

def ktdecompress(filename, stream, address, rawsize, decompressedsize, entryNum):
    origAddress = address
    verification = np.memmap(filename, dtype=int, offset=address, mode='r', shape=(1, 1))
    address += 4
    processedChunks = 4
    decompFile = b''  # Use bytes instead of a string
    endSize = 0
    extension = ''
    if decompressedsize == verification[0]:
        while True:
            compStreamSize = np.memmap(filename, dtype=int, offset=address, mode='r', shape=(1, 1))
            endSize = int(compStreamSize[0])
            if endSize == 0:
                break
            decompFile += zlib.decompress(stream[address + 4:address + 4 + endSize])
            address += endSize + 4
            processedChunks += endSize + 4
        if decompFile[:4] == b'\x47\x54\x31\x47':  # Use bytes instead of a string
            extension = '3ds.g1t'
        elif decompFile[:4] == b'\x5f\x41\x31\x47':  # Use bytes instead of a string
            extension = 'g1a'
        elif decompFile[:4] == b'\x5f\x41\x31\x47':  # Use bytes instead of a string
            extension = 'g2a'
        elif decompFile[:4] == b'\xf2\x7a\x33\x01':  # Use bytes instead of a string
            extension = 'z3'
        elif decompFile[:4] == b'\x4e\x31\x34\x00':  # Use bytes instead of a string
            extension = '41n'
        elif decompFile[:4] == b'\x03\x00\x00\x00':  # Use bytes instead of a string
            extension = 'nfc'
        elif decompFile[:4] == b'\x02\x00\x00\x00':  # Use bytes instead of a string
            extension = 'sdb'
        elif set(decompFile[:4]).issubset(allowedChars):
            extension = decompFile[:4].decode('ascii')  # Convert bytes to string
            if set(decompFile[4:8]).issubset(allowedChars):
                extension = decompFile[:8].decode('ascii')  # Convert bytes to string
        else:
            if ((entryNum >= 53 and entryNum <= 63 and entryNum != 60 and entryNum != 54) or
                    (entryNum >= 13585 and entryNum <= 14264) or
                    (entryNum >= 15132 and entryNum <= 15954 and len(decompFile) > 20) or
                    (entryNum >= 16112 and entryNum <= 16131)):
                extension = 'script'
            else:
                extension = 'unknown'
        with open(path + "%08d-X" % (entryNum,) + "-%08d" % (decompressedsize,) + '.' + extension, 'wb') as fo:
            fo.write(decompFile)
        return decompFile
    else:
        return


def ktextract(filename, stream, address, rawsize, decompressedsize, entryNum):
    extension = ''
    if stream[address:address + 4] == '\x5f\x41\x31\x47':
        extension = 'g1a'
    elif stream[address:address + 4] == '\x5f\x41\x31\x47':
        extension = 'g2a'
    elif stream[address:address + 4] == '\x47\x54\x31\x47':
        extension = '3ds.g1t'
    elif stream[address:address + 4] == '\x1d\x78\x33\x01':
        extension = 'x3'
    elif stream[address:address + 4] == '\xf2\x7a\x33\x01':
        extension = 'z3'
    elif stream[address:address + 4] == '\x4e\x31\x34\x00':
        extension = '41n'
    elif stream[address:address + 4] == '\x03\x00\x00\x00':
        extension = 'nfc'
    elif stream[address:address + 4] == '\x02\x00\x00\x00':
        extension = 'sdb'
    elif set(stream[address:address + 4]).issubset(allowedChars):
        extension = stream[address:address + 4]
        if set(stream[address + 4:address + 8]).issubset(allowedChars):
            extension = stream[address:address + 8]
    else:
        if ((entryNum >= 53 and entryNum <= 63 and entryNum != 60 and entryNum != 54) or
                (entryNum >= 13585 and entryNum <= 14264) or
                (entryNum >= 15134 and entryNum <= 15954 and rawsize > 20) or
                (entryNum >= 16112 and entryNum <= 16131)):
            extension = 'script'
        else:
            extension = 'unknown'
    with open(path + "%08d-U" % (entryNum,) + "-%08d" % (rawsize,) + '.' + extension, 'wb') as fo:
        fo.write(stream[address:address + rawsize])
    return

# Load the file
filename = 'LINKDATA_A.BIN'
with open(filename, 'rb') as f:
    linkData = f.read()

if dword2int(linkData[:4]) == 0x0133781d:  # compare first 4-bytes to the marker
    print('Correct File Found!')
else:
    print('Incorrect File Found... Aborting')
    quit()

sizeTable = dword2int(linkData[4:8]) * 16
numberEntries = sizeTable // 16
mulAddress = dword2int(linkData[8:12])  # address multiplier

print('Size of Table: ' + str(sizeTable))
print('Number of Entries: ' + str(numberEntries))
print('Address multiplier: ' + str(mulAddress))

# Table Structure
# [EntryAddress * 4bytes][Null * 4bytes][sizeOfData * 4 bytes][decompressedSize * 4bytes]
# Note: EntryAddress needs to be multiplied by mulAddress for correct alignment
tableData = np.memmap(filename, dtype=int, offset=16, mode='r', shape=(numberEntries, 4))

path = 'Sangokushi-Xtracted\\'
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

for entryNum in range(numberEntries):
    Offset = tableData[entryNum][0] * mulAddress
    RawSize = tableData[entryNum][2]
    DecompressedSize = tableData[entryNum][3]
    print('Entry#' + str(entryNum) + ' Offset:' + str(hex(Offset)) + ' RawSize:' + str(RawSize) + ' DecompressedSize:' + str(DecompressedSize))
    if DecompressedSize > 0:
        ktdecompress(filename, linkData, Offset, RawSize, DecompressedSize, entryNum)
    else:
        ktextract(filename, linkData, Offset, RawSize, DecompressedSize, entryNum)
