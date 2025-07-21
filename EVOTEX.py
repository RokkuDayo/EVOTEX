import tkinter as tk
from PIL import ImageTk, Image

def aboutWindow():
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
textureMenu.add_command(label="Import DDS as GTX")
textureMenu.add_command(label="Import DDS as GMP")
textureMenu.add_separator()
textureMenu.add_command(label="Export to DDS")

evoMenubar.add_command(label="About", command=aboutWindow)

root.geometry("900x720")
root.title("EVOTEX - Codemasters EVO Texture Tool")
root.iconbitmap("Assets/EVOTEXIcon.ico")
root.config(menu = evoMenubar)

root.mainloop()