# Codemasters EVO Engine Texture Scripts

Python scripts for reading and writing textures for games using the Codemasters EVO engine (DIRT 5 and Onrush).

## Requirements
  - ### Python 3.10+
  - ### Construct (Python module)
 	 - To install Construct, run `pip install Construct` on your terminal.

## Usage
 ### DIRT5_convert_DDS2Game.py
  - `python DIRT5_convert_DDS2Game.py [DDS FILE PATH] [GTX TEXTURE NAME] [GTX TEXTURE PATH].`
    - The [GTX TEXTURE PATH] field stands for where in the game's folder structure the texture will be stored (i.e., `textures/vehicles/alfa_romeo_giulia_gtam/`). Getting this wrong will crash the game.
	- Example: `python DIRT5_convert_DDS2Game.py "mycustomdecal.dds" decal_007 "textures\liveryEditor3\generic\stickers\"`
  - Supported texture types: 2D textures, 3D textures (arrays), and cubemap textures.
  - Supported compression formats: R8, R8G8, R8G8B8A8, R16G16B16A16, BC1, BC2, BC3, BC4, BC5, BC6, BC7. (Must be in the DX10 format)
  
 ### DIRT5-ONRUSH_convert_Game2DDS.py
  - `python DIRT5-ONRUSH_convert_Game2DDS.py [GTX/GMP FILE PATH]`
    - Alternatively, you can use the bundled Windows batch file by dragging & dropping GTX and GMP files onto it.
	- Example: `python DIRT5-ONRUSH_convert_Game2DDS.py "E:\Games\Steam\steamapps\common\DIRT 5\data\patch_wip\textures\liveryEditor3\generic\stickers\decal_007.gtx"`
  - Supports all texture types and compression formats used by the game.
  - GMP files must have their parent GTX file in the same directory to be converted.
