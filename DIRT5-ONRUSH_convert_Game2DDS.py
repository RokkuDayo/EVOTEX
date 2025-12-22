from read_GTXGMP import *
import sys
import struct
import time
import os
import re

def remap(value, remapdict, fail):
    return remapdict.get(value, fail)

remapDXGIFormat = {
    "eR8UNorm": 61,
    "eR8SNorm": 63,
    "eR8UInt": 62,
    "eR8G8UNorm": 49,
    "eR8G8SNorm": 51,
    "eR8G8UInt": 50,
    "eR8G8B8A8sRGB": 29,
    "eR8G8B8A8UNorm": 28,
    "eR8G8B8A8SNorm": 31,
    "eR8G8B8A8UInt": 30,
    "eR16UNorm": 56,
    "eR16SNorm": 58,
    "eR16UInt": 57,
    "eR16Float": 54,
    "eR16G16UNorm": 35,
    "eR16G16SNorm": 37,
    "eR16G16UInt": 36,
    "eR16G16Float": 34,
    "eR16G16B16A16UNorma": 11,
    "eR16G16B16A16SNorm": 13,
    "eR16G16B16A16UInt": 12,
    "eR16G16B16A16Float": 10,
    "eR24UNorm": 46,
    "eR32UInt": 42,
    "eR32Float": 41,
    "eR32G32UInt": 17,
    "eR32G32Float": 16,
    "eR32G32B32A32UInt": 3,
    "eR32G32B32A32Float": 2,
    "eR5G6B5UNorm": 85,
    "eR11G11B10Float": 26,
    "eR10G10B10A2UNorm": 24,
    "eBC1sRGB": 72,
    "eBC1UNorm": 71,
    "eBC2sRGB": 75,
    "eBC2UNorm": 74,
    "eBC3sRGB": 78,
    "eBC3UNorm": 77,
    "eBC4UNorm": 80,
    "eBC4SNorm": 81,
    "eBC5UNorm": 83,
    "eBC5SNorm": 84,
    "eBC6": 94,
    "eBC7sRGB": 99,
    "eBC7UNorm": 98
}

remapTextureType = {
    "Texture": 3,
    "Atlas": 3,
    "unkTexType": 0,
    "Cubemap": 3
}

# This might be the worst way anyone has ever come up with to do this.

ddsSig = b"\x44\x44\x53\x20"
ddsSize = b"\x7C\x00\x00\x00"
ddsFourCC = b"\x44\x58\x31\x30"

ddsRGBAMasks = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

ddsCaps = b"\x08\x10\x40\x00"
ddsPitch = 0
ddsAlphaMode = 0
ddsReserved = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4E\x56\x54\x33\x01\x00\x00\x00\x20\x00\x00\x00"
ddsReserved2 = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

def convertGame2DDS(fileGame):
    fileGameRoot, fileGameExt = os.path.splitext(fileGame)
    fileGameName = os.path.splitext(os.path.basename(fileGame))[0]
    
    if fileGameExt.lower() == ".gmp":
        print("GMP (Game Mip Map) detected.")
        fileGTXofGMP = re.sub(r'_tier\d+$', '', fileGameRoot) + '.gtx'
        if os.path.isfile(fileGTXofGMP):
            print(f"Found parent GTX: {fileGTXofGMP}")
        else:
            print("Failed to find parent GTX.")
            sys.exit()

        dataGTXGame = readGTXGMP(fileGTXofGMP)
        dataGMPGame = readGTXGMP(fileGame)
        dataGameTexType = dataGTXGame.TextureHeader.imageType
    elif fileGameExt.lower() == ".gtx":
        try:
            dataGTXGame = readGTXGMP(fileGame)
        except:
            print("Error: Could not recognize the Texture Conditioner version.")
            sys.exit()
        dataGameTexType = dataGTXGame.TextureHeader.imageType
    else:
        print("Error: Unknown input file.")
        sys.exit()

    # Default values, uncompressed and 2D texture.
    ddsFlags = b"\x0F\x10\x02\x00"
    ddsPfFlags = b"\x04\x00\x00\x00"
    dds3DFlags = b"\x00\x00\x00\x00"
    ddsMiscFlags = b"\x00\x00\x00\x00"
    ddsArraySize = 1

    if dataGameTexType == "Cubemap":
        dds3DFlags = b"\x00\xFE\x00\x00"
        ddsMiscFlags = b"\x04\x00\x00\x00"

    if dataGameTexType == "Atlas":
        ddsArraySize = dataGTXGame.TextureHeader.imageDepth

    if dataGTXGame.TextureHeader.dxgiFormat in ("eBC1sRGB", "eBC1UNorm", "eBC2sRGB", "eBC2UNorm", "eBC3sRGB", "eBC3UNorm", "eBC4UNorm", "eBC4SNorm", "eBC5UNorm", "eBC5SNorm", "eBC6", "eBC7sRGB", "eBC7UNorm"):
        ddsFlags = b"\x07\x10\x0A\x00"

    dataGameDepth = dataGTXGame.TextureHeader.imageDepth
    dataGameMips = dataGTXGame.TextureHeader.imageMipLevels

    if fileGameExt.lower() == ".gtx":
        dataGameHeight = dataGTXGame.TextureHeader.imageHeight
        dataGameWidth = dataGTXGame.TextureHeader.imageWidth
        dataGameDDSRaw = dataGTXGame.DDSData

    if fileGameExt.lower() == ".gmp":
        dataGameHeight = dataGMPGame.TextureHeader.imageHeight
        dataGameWidth = dataGMPGame.TextureHeader.imageWidth
        dataGameDDSRaw = dataGMPGame.DDSData

    dataGameDXVer = remap(dataGTXGame.TextureHeader.dxgiFormat, remapDXGIFormat, 99)
    dataGameDXType = remap(dataGTXGame.TextureHeader.imageType, remapTextureType, 0)

    dataDDSFinalBytes = (ddsSig + ddsSize + ddsFlags
                + struct.pack("iiiii", dataGameHeight, dataGameWidth, ddsPitch, dataGameDepth, dataGameMips)
                + ddsReserved + ddsPfFlags + ddsFourCC + ddsRGBAMasks + ddsCaps + dds3DFlags + ddsReserved2
                + struct.pack("ii", dataGameDXVer, dataGameDXType)
                + ddsMiscFlags
                + struct.pack("ii", ddsArraySize, ddsAlphaMode)
                + dataGameDDSRaw)

    with open(f"{fileGameName}" + ".dds", 'wb') as file:
        file.write(dataDDSFinalBytes)

if len(sys.argv) > 1:
    try:
        convertGame2DDS(sys.argv[1])
    except:
        print("Error: File not found.")
        sys.exit()
    print("Conversion complete!")
else:
    print("Error: No file passed as an argument.")
    print("Usage: python convert_GAME2DDS.py [GTX FILE PATH]")
    time.sleep(3)
