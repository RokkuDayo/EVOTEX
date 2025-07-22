from read_GTXGMP import *
import struct

def remap(value, remapdict, fail):
    return remapdict.get(value, fail)

dx_ver_remap = {
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

dx_type_remap = {
    "Texture": 3,
    "Atlas": 4,
    "unkTexType": 0,
    "Cubemap": 4
}

#This might be the worst way to do this but it works in my head.

ddsSig = b"\x44\x44\x53\x20"
ddsSize = b"\x7C\x00\x00\x00"
ddsFlags = b"\x07\x10\x0A\x00"
ddsMisc = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4E\x56\x54\x33\x01\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00\x44\x58\x31\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
ddsPitch = 0
ddsFlagsPad = 0
ddsArraySize = 0
ddsAlphaMode = 0

def convertGTX2DDS(fileGTX):
    gameTexData = readGTXGMP(fileGTX)

    gameHeight = gameTexData.TextureHeader.imageHeight
    gameWidth = gameTexData.TextureHeader.imageWidth
    gameDepth = gameTexData.TextureHeader.imageDepth
    gameMips = gameTexData.TextureHeader.imageMipLevels
    gameDXVer = remap(gameTexData.TextureHeader.dxgiFormat, dx_ver_remap, 99)
    gameDXType = remap(gameTexData.TextureHeader.imageType, dx_type_remap, 0)

    ddsByteData = (ddsSig + ddsSize + ddsFlags
                + struct.pack("iiiii", gameHeight, gameWidth, ddsPitch, gameDepth, gameMips)
                + ddsMisc + struct.pack("iiiii", gameDXVer, gameDXType, ddsFlagsPad, ddsArraySize, ddsAlphaMode)
                + gameTexData.DDSData)

    with open(f"{gameTexData.TextureHeader.fileName}.dds", 'wb') as file:
        file.write(ddsByteData)

#convertGTX2DDS("Samples/startScreen_Amplified.gtx")