from read_DDS import *
import sys

convDXGIFormatToEVOFormat = {
    61: 0,   # R8_UNORM > eR8UNorm
    62: 2,   # R8_UINT > eR8UInt
    63: 1,   # R8_SNORM > eR8SNorm

    3: 49,   # R8G8_UNORM > eR8G8UNorm
    5: 50,   # R8G8_UINT > eR8G8UInt
    4: 51,   # R8G8_SNORM > eR8G8SNorm

    28: 7,   # R8G8B8A8_UNORM  > eR8G8B8A8UNorm
    29: 6,   # R8G8B8A8_UNORM_SRGB > eR8G8B8A8sRGB
    30: 9,   # R8G8B8A8_UINT > eR8G8B8A8UInt
    31: 8,   # R8G8B8A8_SNORM > eR8G8B8A8SNorm

    11: 18,   # R16G16B16A16_UNORM  > eR16G16B16A16UNorma
    13: 19,   # R16G16B16A16_SNORM > eR16G16B16A16SNorm
    12: 20,   # R16G16B16A16_UINT > eR16G16B16A16UInt
    10: 21,   # R16G16B16A16_FLOAT > eR16G16B16A16Float

    71: 33,  # BC1_UNORM > eBC1UNorm
    72: 32,  # BC1_UNORM_SRGB > eBC1sRGB

    74: 35,  # BC2_UNORM > eBC2UNorm
    75: 34,  # BC2_UNORM_SRGB > eBC2sRGB

    77: 37,  # BC3_UNORM > eBC3UNorm
    78: 36,  # BC3_UNORM_SRGB > eBC3sRGB

    80: 38,  # BC4_UNORM > eBC4UNorm
    81: 39,  # BC4_SNORM > eBC4SNorm

    83: 40,  # BC5_UNORM > eBC5UNorm
    84: 41,  # BC5_SNORM > eBC5SNorm

    94: 42,  # BC6H_TYPELESS > eBC6
    95: 42,  # BC6H_UF16 > eBC6
    96: 42,  # BC6H_SF16 > eBC6

    98: 44,  # BC7_UNORM > eBC7UNorm
    99: 43,  # BC7_UNORM_SRGB > eBC7sRGB
}

class decompMiscFlags:
    def __init__(self, value):
        self.value = value

    @property
    def textureCube(self):
        return bool(self.value & (1 << 2))

    @property
    def generateMips(self):
        return bool(self.value & (1 << 0))

    @property
    def shared(self):
        return bool(self.value & (1 << 1))

def normalizeGTXPath(s: str) -> str:
    if s.startswith(('/', '\\')):
        s = s[1:]

    if not s.endswith('\\'):
        s += '\\'

    return s.replace('\\', '/')

def hashFNV(name):
    while True:
        s = name.encode("utf-8")
        
        fnv_offset = 0xcbf29ce484222325
        fnv_prime = 0x100000001b3
        h = fnv_offset
        for c in s:
            h ^= c
            h = (h * fnv_prime) & 0xFFFFFFFFFFFFFFFF
        
        finalValue = h.to_bytes(8, 'little')
    
        return(finalValue)

def convertGame2DDS(fileDDS, nameGTX, pathGTX):
    headerGTX = b"\x20\x4F\x56\x45\x01\x00\x00\x00\x52\x44\x48\x4D\x0D\x00\x00\x00\x4D\x41\x53\x54\x45\x52\x20\x48\x45\x41\x44\x45\x52\x04\x00\x00\x00\x9C\x9A\xAD\x69\xBB\x87\xB8\x2A\x2B\x00\x00\x00\x01\x00\x00\x00\x42\x4C\x58\x50\x01\x00\x00\x00\x12\x54\x65\x78\x74\x75\x72\x65\x43\x6F\x6E\x64\x69\x74\x69\x6F\x6E\x65\x72\x07\x31\x2E\x30\x2E\x30\x2E\x30\x00\x00\x00\x00\x42\x4C\x58\x50"

    pathGTXNormalized = f"data:{normalizeGTXPath(pathGTX)}"

    hashFilename = hashFNV(nameGTX)

    dataDDS = readDDS(fileDDS)
    if dataDDS.fourCC != "DX10":
        print("Error: Extended DirectX 10 header missing. This tool is not compatible with DDS files made for DirectX 9 and below.")
        sys.exit()

    try:
        keyDXGI = convDXGIFormatToEVOFormat[int(dataDDS.dxgiFormat)]
    except:
        print("Error: Unsupported DXGI compression format.")
        sys.exit()

    dataDDSFlags = decompMiscFlags(dataDDS.miscFlags)
    if dataDDSFlags.textureCube:
        dataDDSTextureType = (b"\x03\x00\x00\x00") # Cubemap texture.
    elif dataDDS.arraySize > 1:
        dataDDSTextureType = (b"\x01\x00\x00\x00") # Atlas texture.
    else:
        dataDDSTextureType = (b"\x00\x00\x00\x00") # Normal texture.
    
    dataGTXPlaceholder = (headerGTX
               + len(nameGTX).to_bytes(4, byteorder='little')
               + nameGTX.encode(encoding="utf-8")
               + (b"\x0A\x00\x00\x00")
               + hashFilename
               + (112 + len(nameGTX)).to_bytes(4, byteorder='little') # Length of everything before it.
               + dataDDSTextureType
               + dataDDS.width.to_bytes(4, byteorder='little')
               + dataDDS.height.to_bytes(4, byteorder='little')
               + dataDDS.arraySize.to_bytes(4, byteorder='little')
               + dataDDS.mipMapLevels.to_bytes(4, byteorder='little')
               + keyDXGI.to_bytes(4, byteorder='little')
               + hashFilename
               + (len(nameGTX) + 8 + 1).to_bytes(4, byteorder='little')
               + hashFilename
               + nameGTX.encode(encoding="utf-8")
               + (b"\x00")
               + len(pathGTXNormalized).to_bytes(1, byteorder='little')
               + pathGTXNormalized.encode(encoding="utf-8")
               + dataDDS.mipMapLevels.to_bytes(4, byteorder='little')
               + dataDDS.width.to_bytes(4, byteorder='little')
               + dataDDS.height.to_bytes(4, byteorder='little')
               + (b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00") # No support for generating GMPs, at least not for now.
               + len(dataDDS.ImageData).to_bytes(4, byteorder='little')
               + dataDDS.ImageData
               )
    # This is a waste but I don't know how else to get the full size of the file to then subtract it from one of the offset values.

    dataGTX = (headerGTX
               + len(nameGTX).to_bytes(4, byteorder='little')
               + nameGTX.encode(encoding="utf-8")
               + (b"\x0A\x00\x00\x00")
               + hashFilename
               + (len(dataGTXPlaceholder) - (112 + len(nameGTX))).to_bytes(4, byteorder='little') # Length of everything before it.
               + dataDDSTextureType
               + dataDDS.width.to_bytes(4, byteorder='little')
               + dataDDS.height.to_bytes(4, byteorder='little')
               + dataDDS.arraySize.to_bytes(4, byteorder='little')
               + dataDDS.mipMapLevels.to_bytes(4, byteorder='little')
               + keyDXGI.to_bytes(4, byteorder='little')
               + hashFilename
               + (len(nameGTX) + 8 + 1).to_bytes(4, byteorder='little')
               + hashFilename
               + nameGTX.encode(encoding="utf-8")
               + (b"\x00")
               + len(pathGTXNormalized).to_bytes(1, byteorder='little')
               + pathGTXNormalized.encode(encoding="utf-8")
               + dataDDS.mipMapLevels.to_bytes(4, byteorder='little')
               + dataDDS.width.to_bytes(4, byteorder='little')
               + dataDDS.height.to_bytes(4, byteorder='little')
               + (b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00") # No support for generating GMPs, at least not for now.
               + len(dataDDS.ImageData).to_bytes(4, byteorder='little')
               + dataDDS.ImageData
               )

    with open(f"{nameGTX}.gtx", 'wb') as file:
        file.write(dataGTX)

if len(sys.argv) > 1:
    try:
        convertGame2DDS(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Error: Input and/or arguments not found.")
        sys.exit()
    print("")
    print("Conversion from DDS to GTX complete!")
else:
    print("Error: No files and paths passed as arguments.")
    print("Usage: python convert_DDS2Game.py [DDS FILE PATH] [GTX TEXTURE NAME] [GTX TEXTURE PATH]")
    print("The [GTX TEXTURE PATH] stands for where in the game's root folder the texture will be stored.")
    print("Example: textures/vehicles/alfa_romeo_giulia_gtam/")