from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image

def raiseFrame(frame):
    frame.tkraise()

# opens the file and gets the file name used for the image
def openFile():
    global file
    file = askopenfile(mode = 'r')
    file = file.name
    if file is not None:
        pass

# converts the image to ascii characters and displays
def convertFile():
    # create another window
    window = Toplevel()
    window.config(bg = BG)
    
    # error handling
    errorLabel = Label(window, font = ("Courier", 20), bg = BG, fg = FG)
    # checks if input is an integer
    try:
        artW = int(currentWidth.get())
        fontSize = int(currentFontSize.get())
    except:
        errorLabel.config(text = "Invalid value for width/font size!")
        errorLabel.grid(row = 0, column = 0, padx = 3, pady = 3)
        return
    # checks if file is given
    if file == "":
        errorLabel.config(text = "No file given!")
        errorLabel.grid(row = 0, column = 0, padx = 3, pady = 3)
        return
    # checks if file is image
    try:
        img = Image.open(file).convert("RGB")
    except:
        errorLabel.config(text = "Can't process file type!")
        errorLabel.grid(row = 0, column = 0, padx = 3, pady = 3)
        return
        
    density = " .:-=+*#%@"
    if inverted.get():
        density = density[::-1]
    w,h = img.size
    artH = int(((artW / w) * h) * .5)
    img = img.resize((artW, artH))
    
    # creates art string by going through each pixel
    art = "```\n"
    for y in range(0, artH):
        for x in range(0, artW):
            r,g,b = img.getpixel((x, y))
            # get subjective brightness and map to density value
            brightness = (.21 * r + .72 * g + .07 * b)
            art += density[int(brightness // (255 / len(density)))]
        art += "\n"
    art += "```"
    
    # copy art to clipboard
    root.clipboard_clear()
    root.clipboard_append(art)
    # display art
    artLabel = Label(window, text = art[3:len(art) - 3], font = ("Courier", fontSize), bg = BG, fg = FG)
    artLabel.grid(row = 0, column = 0, padx = 10, pady = 10)
    
file = ""  
# create GUI
BG = "#232429"
FG = "white"
root = Tk()
root.title("Ascii Art Generator")
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)
home = Frame(root, bg = BG)
home.grid(row = 0, column = 0, sticky = "nsew")
fileLabel = Label(home, text = "Upload image: ", font = ("Courier", 10), bg = BG, fg = FG, anchor = "e")
fileLabel.grid(row = 0, column = 0, columnspan = 2, sticky = "e")
fileButton = Button(home, text = "Choose File", command = lambda:openFile(), font = ("Courier", 10), bg = BG, fg = FG, anchor = "w")
fileButton.grid(row = 0, column = 2, columnspan = 2, sticky = "w")
widthLabel = Label(home, text = "Art Width: ", font = ("Courier", 10), bg = BG, fg = FG, anchor = "e")
widthLabel.grid(row = 1, column = 0, columnspan = 2, sticky = "e")
currentWidth = StringVar(value = 100)
widthSpinbox = Spinbox(home, from_ = 10, to_ = 1000, textvariable = currentWidth, wrap = True, bg = BG, fg = FG)
widthSpinbox.grid(row = 1, column = 2, columnspan = 2, sticky = "w")
fontSizeLabel = Label(home, text = "Art Font Size: ", font = ("Courier", 10), bg = BG, fg = FG, anchor = "e")
fontSizeLabel.grid(row = 2, column = 0, columnspan = 2, sticky = "e")
currentFontSize = StringVar(value = 10)
fontSizeSB = Spinbox(home, from_ = 1, to_ = 20, textvariable = currentFontSize, wrap = True, bg = BG, fg = FG)
fontSizeSB.grid(row = 2, column = 2, columnspan = 2, sticky = "w")
inverted = BooleanVar()
invertButton = Checkbutton(home, text = "Inverted", font = ("Courier", 10), bg = BG, fg = FG, variable = inverted, onvalue = True, offvalue = False, selectcolor = BG)
invertButton.grid(row = 3, column = 1, columnspan = 2)
convertButton = Button(home, text = "Convert Image", command = lambda:convertFile(), font = ("Courier", 20), bg = BG, fg = FG)
convertButton.grid(row = 4, column = 1, columnspan = 2, pady = 15)

root.mainloop()