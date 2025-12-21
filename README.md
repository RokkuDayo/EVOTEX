<p align="center">
  <img src="Assets/EVOTEXLogo.png" width="200" />
</p>

# EVOTEX | Codemasters EVO Texture Tool

Python scripts for reading and writing textures for games using the Codemasters EVO engine (DIRT 5 and Onrush).

## Requirements:
 ### Python 3.10+ and the Construct module.
  - To install Construct, simply run [pip install Construct]

## Usage
 ### DIRT5_convert_DDS2Game.py
  - python convert_DDS2Game.py [DDS FILE PATH] [GTX TEXTURE NAME] [GTX TEXTURE PATH]
    - The [GTX TEXTURE PATH] stands for where in the game's root folder the texture will be stored. This is important to get right otherwise the game will crash.
	- Example: textures/vehicles/alfa_romeo_giulia_gtam/
  
  - Supported texture types: 2D textures, 3D textures (arrays), and cubemap textures.
  - Supported compression formats: R8, R8G8, R8G8B8A8, R16G16B16A16, BC1, BC2, BC3, BC4, BC5, BC6, BC7. (Must be in the DX10 format)
  
 ### DIRT5-ONRUSH_convert_Game2DDS.py
  - python DIRT5-ONRUSH_convert_Game2DDS.py [GTX/GMP FILE PATH]
    - Alternatively, you can use the bundled Windows batch file by simply drag & dropping GTX and GMP files onto it.
  - Supports all texture types and compression formats used by the game.
  - GMP files must have their parent GTX file in the same directory to be converted.
