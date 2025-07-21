import type.base;

enum DXGI_FORMAT : u32 {
    eR8UNorm,
    eR8SNorm,
    eR8UInt,
    eR8G8UNorm,
    eR8G8SNorm,
    eR8G8UInt,
    eR8G8B8A8sRGB,
    eR8G8B8A8UNorm,
    eR8G8B8A8SNorm,
    eR8G8B8A8UInt,
    eR16UNorm,
    eR16SNorm,
    eR16UInt,
    eR16Float,
    eR16G16UNorm,
    eR16G16SNorm,
    eR16G16UInt,
    eR16G16Float,
    eR16G16B16A16UNorma,
    eR16G16B16A16SNorm,
    eR16G16B16A16UInt,
    eR16G16B16A16Float,
    eR24UNorm,
    eR32UInt,
    eR32Float,
    eR32G32UInt,
    eR32G32Float,
    eR32G32B32A32UInt,
    eR32G32B32A32Float,
    eR5G6B5UNorm,
    eR11G11B10Float,
    eR10G10B10A2UNorm,
    eBC1sRGB,
    eBC1UNorm,
    eBC2sRGB,
    eBC2UNorm,
    eBC3sRGB,
    eBC3UNorm,
    eBC4UNorm,
    eBC4SNorm,
    eBC5UNorm,
    eBC5SNorm,
    eBC6,
    eBC7sRGB,
    eBC7UNorm
};

enum TEX_TYPE : u32 {
    Texture,
    Atlas,
    unkTexType,
    Cubemap
};

struct header_t {
    char sigMaster[29];
    u32 unk1;
    u32 unk2;
    u32 unk3;
    u32 texCondLength;
    char texCondSig[texCondLength];
};

struct headerGTX_t {
    u32 fileNameLength;
    char fileName[fileNameLength];
    u32 unk1;
    be type::Hex<u64> FNV_1;
    be type::Hex<u32> unk2; // Not sure but the same value is used in textures that belong to the same texture set. Setting it all to zeroes crashes the game. Could have something to do with the "usageHint" mentioned in the strings for Onrush.
    TEX_TYPE textureType;
    u32 imageWidth;
    u32 imageHeight;
    u32 imageDepth; // Corresponds to the amount of slices in cubemaps and slices in an atlas.
    u32 mipMapCount;
    DXGI_FORMAT dxgiFormat;
    be type::Hex<u64> FNV_2;
    u32 lengthToPathLength; // Length of FNV + FILENAME + SEPARATOR
    be type::Hex<u64> FNV_3;
    char fileName2[fileNameLength];
    be type::Hex<u8> separator; // It's always set to 00 so I presume its some kind of padding or separator.
    u8 filePathLength;
    char filePath[filePathLength];
    u32 imageMipLevelsMax; 
    u32 imageWidthMax;
    u32 imageHeightMax;
    u32 unk7;
    u32 imageTierCount; // How many extra GMP files this GTX will have. Seems to be set to 0 in some textures despite them having extra tiers?
    u32 unk9;
    //Unsure why the below works that way.
    if (unk1 == 9) {
        u32 unkExtra;
        u32 DDSDataLength;
    }
    else if (unk1 == 10) {
        u32 DDSDataLength;
    }
};

struct headerGMP_t {
    u32 fileNameLength;
    char fileName[fileNameLength];
    u32 unk1; // Probably the length for something.
    be type::Hex<u64> FNV_1;
    u32 unk2; // Always set to 3 in every GMP I checked.
    u32 imageWidth;
    u32 imageHeight;
    u32 imageDepth; // Corresponds to the amount of slices in cubemaps and slices in an atlas.
    u32 imageTierNumber; // This counts backwards for each mipmap tier. Usually has 2 for tier 1, 1 for tier 2, and 0 for tier 3.
    DXGI_FORMAT dxgiFormat;
    be type::Hex<u64> FNV_2;
    u8 fileName2Length;
    char fileName_2[fileName2Length];
    be type::Hex<u64> fileGTX_FNV; // FNV for the GTX this GMP belongs to.
    u8 fileGTXNameLength; // Name of the GTX this GMP belongs to.
    char fileGTXName[fileGTXNameLength];
    u32 DDSDataLength;
} [[comment("GMP Mipmap Header")]];

struct fileType_t {
    char sigGTXorGMP[4] @ sizeof(header);
    if (sigGTXorGMP == "BLXP") {
    headerGTX_t headerGTX @ (sizeof(header) + 4);
    }
    else if (sigGTXorGMP == "BPIM") {
        headerGMP_t headerGMP @ (sizeof(header) + 4);
    }
};

struct data_t {
    u32 dataLength;
    char data[dataLength];
};

u32 headersize;

header_t header @ 0x00 [[comment("EVO Master Header")]];
fileType_t fileType @ sizeof(header);