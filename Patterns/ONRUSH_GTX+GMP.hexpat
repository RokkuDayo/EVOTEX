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
eBC7UNorm,
eZ16,
eZ32,
eZ24S8,
eZ32S8,
eDisplaySDR,
eDisplayHDR,
sPlarJghargh,
eUnknown,
eX32Float,
eX32Y32Float,
eX32Y32Z32Float,
eX32Y32Z32W32Float,
eX10Y10Z10SNorm,
eX11Y11Z10Float,
eX8Y8Z8W8UNorm,
eX8Y8Z8W8SNorm,
eX8Y8Z8W8UInt,
eX32UInt,
eX16Float,
eX16Y16Float,
eX16Y16Z16Float,
eX16Y16Z16W16Float,
eX16UNorm,
eX16Y16UNorm,
eX16Y16Z16UNorm,
eX16Y16Z16W16UNorm
};

struct header_t {
    char sigMaster[29];
    u32 unk1;
    u32 unk2;
    u32 unk3;
    u32 texCondLength;
    char texCondSig[texCondLength];
    char sigGTXorGMP[4];
    u32 fileNameLength;
    char fileName[fileNameLength];
    u32 unk4;
    u64 FNV_1;
    u16 unk5;
    u32 unk6;
    u16 unk7;
    u32 imageWidth;
    u32 imageHeight;
    u32 unk8;
    u32 mipMapCount;
    DXGI_FORMAT dxgiFormat;
    u64 FNV_2;
    u32 lengthToPathLength; // FNV + FILENAME + UNK (Separator?)
    u64 FNV_3;
    char fileName2[fileNameLength]; // This is ass. Check GMP.
    u8 unk10;
    u8 filePathLength;
    char filePath[filePathLength];
    u32 mipMapCount2;
    u32 imageWidth2;
    u32 imageHeight2;
    u32 unk12;
    u32 unk13;
    u32 unk14;
};

struct data_t {
    u32 dataLength;
    char data[dataLength];
};

u32 headersize;

header_t header @ 0x00 [[comment("EVO Master Header")]];
headersize = sizeof(header);
data_t data @ headersize [[comment("Raw DDS Data")]];