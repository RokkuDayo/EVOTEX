import tkinter as tk
from PIL import ImageTk, Image

def aboutWindow():
    about = tk.Tk()
    about.title("About")
    about.geometry("400x300")
    about.eval('tk::PlaceWindow . center')
    about.attributes('-toolwindow', True)
    about.resizable(False, False) 
    about.iconbitmap("Assets/EVOTEXLogo.ico")

    aboutText = tk.Label(about, text="A tool for texture formats in the Codemasters EVO engine.")
    aboutText.pack()

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
textureMenu.add_command(label="Import from DDS")
textureMenu.add_command(label="Export to DDS")

evoMenubar.add_command(label="About", command=aboutWindow)

root.geometry("900x720")
root.title("EVOTEX - DIRT 5 & Onrush Texture Tool")
root.iconbitmap("Assets/EVOTEXLogo.ico")
root.config(menu = evoMenubar)

root.mainloop()