import struct
import sys
num = float(sys.argv[1])
print struct.pack('<d',num).encode('hex_codec')