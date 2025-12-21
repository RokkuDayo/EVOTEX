from construct import *

TEX_TYPE = Enum(Int32ul,
    Texture = 0,
    Atlas = 1,
    unkTexType = 2, # Can't find a texture that uses 2 or another number.
    Cubemap = 3
)

DXGI_FORMAT = Enum(Int32ul,
    eR8UNorm = 0,
    eR8SNorm = 1,
    eR8UInt = 2,
    eR8G8UNorm = 3,
    eR8G8SNorm = 4,
    eR8G8UInt = 5,
    eR8G8B8A8sRGB = 6,
    eR8G8B8A8UNorm = 7,
    eR8G8B8A8SNorm = 8,
    eR8G8B8A8UInt = 9,
    eR16UNorm = 10,
    eR16SNorm = 11,
    eR16UInt = 12,
    eR16Float = 13,
    eR16G16UNorm = 14,
    eR16G16SNorm = 15,
    eR16G16UInt = 16,
    eR16G16Float = 17,
    eR16G16B16A16UNorma = 18, # Typo comes from the strings found in Onrush.
    eR16G16B16A16SNorm = 19,
    eR16G16B16A16UInt = 20,
    eR16G16B16A16Float = 21,
    eR24UNorm = 22,
    eR32UInt = 23,
    eR32Float = 24,
    eR32G32UInt = 25,
    eR32G32Float = 26,
    eR32G32B32A32UInt = 27,
    eR32G32B32A32Float = 28,
    eR5G6B5UNorm = 29,
    eR11G11B10Float = 30,
    eR10G10B10A2UNorm = 31,
    eBC1sRGB = 32,
    eBC1UNorm = 33,
    eBC2sRGB = 34,
    eBC2UNorm = 35,
    eBC3sRGB = 36,
    eBC3UNorm = 37,
    eBC4UNorm = 38,
    eBC4SNorm = 39,
    eBC5UNorm = 40,
    eBC5SNorm = 41,
    eBC6 = 42,
    eBC7sRGB = 43,
    eBC7UNorm = 44
)

header_Master = Struct(
    "sigMaster"           / Bytes(29),
    
    "unk1"                / Int32ul,
    "unk2"                / Int32ul,
    "unk3"                / Int32ul,

    "texCondLength"       / Int32ul,
    "texCondSig"          / Bytes(this.texCondLength)
)

header_GTX_DIRT5 = Struct(
    "fileNameLength"      / Int32ul,
    "fileName"            / PaddedString(this.fileNameLength, "utf8"),

    "unk1"                / Int32ul,

    "FNV_1"               / Bytes(8),

    "unk2"                / Int32ub,

    "imageType"           / TEX_TYPE,
    "imageWidth"          / Int32ul,
    "imageHeight"         / Int32ul,
    "imageDepth"          / Int32ul, # Corresponds to the amount of slices in cubemaps and slices in an atlas.
    "imageMipLevels"      / Int32ul,

    "dxgiFormat"          / DXGI_FORMAT,

    "FNV_2"               / Bytes(8),

    "offsetToFilePathLength" / Int32ul, # Length of FNV + FILENAME + SEPARATOR
    
    "FNV_3"               / Bytes(8),

    "fileName_2"          / PaddedString((this.fileNameLength), "utf8"),
    "separator"           / Bytes(1),  # It's always set to 0x00 so I presume it's some kind of padding or separator.
    "filePathLength"      / Int8ul,
    "filePath"            / PaddedString((this.filePathLength), "utf8"),

    "imageMipLevelsMax"   / Int32ul, # Amount of mipmaps in last GMP tier.
    "imageWidthMax"       / Int32ul, # Width of the last GMP tier.
    "imageHeightMax"      / Int32ul, # Height of the last GMP tier.
    "unk4"                / Int32ul,
    "imageTierCount"      / Int32ul, # Amount of extra GMP tiers. Seems to be set to 0 in some textures despite them having extra tiers?
    "unk5"                / Int32ul, # This could be the image's repeat mode as there's mentions of that being an option in Onrush's executable
                          # (WRAP, MIRROR, CLAMP, BORDER, MIRROR_ONCE, COUNT), but it's hard to check when I couldn't find an instance of this value being anything but zero.
    
    "unkExtra"            / If(this.unk1 == 9, Int32ul),
)

header_GTX_ONRUSH = Struct(
    "fileNameLength"      / Int32ul,
    "fileName"            / PaddedString(this.fileNameLength, "utf8"),

    "unk1"                / Int32ul,

    "FNV_1"               / Bytes(8),

    "unk2"                / Int32ub,

    "imageType"           / TEX_TYPE,
    "imageWidth"          / Int32ul,
    "imageHeight"         / Int32ul,
    "imageDepth"          / Int32ul, # Corresponds to the amount of slices in cubemaps and slices in an atlas.
    "imageMipLevels"      / Int32ul,

    "dxgiFormat"          / DXGI_FORMAT,

    "FNV_2"               / Bytes(8),

    "fileNameLength_2"    / Int8ul,
    "fileName_2"          / PaddedString((this.fileNameLength_2), "utf8"),
    "filePathLength"      / Int8ul,
    "filePath"            / PaddedString((this.filePathLength), "utf8"),

    "imageMipLevelsMax"   / Int32ul, # Amount of mipmaps in last GMP tier.
    "imageWidthMax"       / Int32ul, # Width of the last GMP tier.
    "imageHeightMax"      / Int32ul, # Height of the last GMP tier.
    "unk4"                / Int32ul,
    "imageTierCount"      / Int32ul, # Amount of extra GMP tiers. Seems to be set to 0 in some textures despite them having extra tiers?
    "unk5"                / Int32ul, # This could be the image's repeat mode as there's mentions of that being an option in Onrush's executable
                          # (WRAP, MIRROR, CLAMP, BORDER, MIRROR_ONCE, COUNT), but it's hard to check when I couldn't find an instance of this value being anything but zero.
    
    "unkExtra"            / If(this.unk1 == 9, Int32ul),
)

header_GMP = Struct(
    "fileNameLength"      / Int32ul,
    "fileName"            / PaddedString(this.fileNameLength, "utf8"),

    "unk1"                / Int32ul,

    "FNV_1"               / Bytes(8),

    "unk2"                / Int32ul,

    "imageWidth"          / Int32ul,
    "imageHeight"         / Int32ul,
    "imageDepth"          / Int32ul,
    "imageTierNumber"     / Int32ul,

    "dxgiFormat" / DXGI_FORMAT,

    "FNV_2" / Bytes(8),

    "fileName2Length"     / Int8ul,
    "fileName_2"          / PaddedString((this.fileName2Length), "utf8"),

    "fileGTX_FNV"         / Bytes(8),
    "fileGTXNameLength"   / Int8ul,
    "fileGTXName"         / PaddedString((this.fileGTXNameLength), "utf8"),
)

header_Full = Struct(
    "EVOMasterHeader"   / header_Master,
    "sigGTXorGMP"         / PaddedString(4, "utf8"),
    "TextureHeader"       / Switch(this.sigGTXorGMP, {
        "BLXP": Switch(this.EVOMasterHeader.texCondLength, {
            43: header_GTX_DIRT5,
            47: header_GTX_ONRUSH,
        }, default=header_GTX_DIRT5),
        "BPIM": header_GMP,
    }, default=Pass),
    "DDSDataLength"       / Int32ul,
    "DDSData"             / Bytes(this.DDSDataLength)
)

def readGTXGMP(fileGTXGMP):
    with open(fileGTXGMP, "rb") as f:
        evoTexData = header_Full.parse_stream(f)
        return(evoTexData)

#if len(sys.argv) > 1:
#    print(readGTXGMP(sys.argv[1]))
#    print("Conversion complete!")
#else:
#    print("No file passed as an argument.")
#    print("Usage: python read_GTXGMP.py [GTX/GMP FILE PATH]")
