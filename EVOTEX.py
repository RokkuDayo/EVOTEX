import imageio
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

def EVOTEX_openFile(extName):
    filepath = filedialog.askopenfilename(filetypes=[(f"{extName} files", f"*.{extName}")])
    if filepath:
        try:
            ddsImg = EVOTEX_loadDDS(filepath)
            ddsImg.thumbnail((800, 800))
            ddsTk = ImageTk.PhotoImage(ddsImg)
            textureDisplay.config(image = ddsTk)
            textureDisplay.image = ddsTk
            root.title(f"EVOTEX - Viewing: {filepath}")
        except Exception as e:
            print(f"Failed to load image: {e}")

def EVOTEX_loadDDS(ddsPath):
    ddsTex = imageio.v2.imread(ddsPath)
    return (Image.fromarray(ddsTex))

def EVOTEX_menuBar():
    evoMenubar = tk.Menu(root)
    fileMenu = tk.Menu(evoMenubar, tearoff=0)
    textureMenu = tk.Menu(evoMenubar, tearoff=0)
    evoMenubar.add_cascade(label="File", menu=fileMenu)

    fileMenu.add_command(label="Open GTX/GMP File")
    fileMenu.add_command(label="Close Current File")
    fileMenu.add_separator()
    fileMenu.add_command(label="Export to GTX")
    fileMenu.add_command(label="Export to GMP")
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=quit)

    evoMenubar.add_cascade(label="Texture", menu=textureMenu)
    textureMenu.add_command(label="Import DDS", command=lambda: EVOTEX_openFile("dds"))
    textureMenu.add_command(label="Export to DDS")

    evoMenubar.add_command(label="About", command=EVOTEX_aboutWindow)

    root.config(menu = evoMenubar)

def EVOTEX_aboutWindow():
    about = tk.Tk()
    about.title("About")
    about.geometry("400x300")
    about.eval('tk::PlaceWindow . center')
    about.attributes('-toolwindow', True)
    about.resizable(False, False) 
    about.iconbitmap("Assets/EVOTEXIcon.ico")

    aboutText = tk.Label(about, text="A tool for texture formats in the Codemasters EVO engine.")
    aboutText.pack()

    aboutGTXText = tk.Label(about, text="GTX files contain the texture and its properties.")
    aboutGTXText.pack()

    aboutGMPText = tk.Label(about, text="GMP files store aditional resolution tiers for a GTX file.")
    aboutGMPText.pack()

root = tk.Tk()

EVOTEX_menuBar()

textureDisplay = tk.Label(root)
textureDisplay.pack(expand=True)

root.geometry("900x720")
root.title("EVOTEX - Codemasters EVO Texture Tool")
root.iconbitmap("Assets/EVOTEXIcon.ico")

root.mainloop()