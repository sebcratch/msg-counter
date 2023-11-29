import os
import shutil
from tkinter import filedialog
from tkinter import *
from zipfile import ZipFile

def autoFind():
    #dialog wybór folderu z zipami
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()

    #na wyjściowe dane
    os.mkdir("data")

    #nikomu niepotrzeby chuj
    chuj = 0
    fb = "/your_activity_across_facebook/messages/inbox/"


    #wybór każdego zipa

        #wypakuj baranie
       # filen = h
        #with ZipFile(folder_selected+'/'+filen, "r") as zip:
         #   print('Extracting all the files now...') 
          #  zip.extractall() 
           # print('Done!') 



    a = os.listdir(''.join([folder_selected, fb]))
    for i in a:
        addDir = input(i[:i.index("_")]+" ")
        if addDir == "y":
            for subFile in os.listdir(''.join([folder_selected, fb, i])):
                if subFile.endswith(".json"):
                    os.rename(''.join([folder_selected, fb, i, '/', subFile]), ''.join([folder_selected, fb, i, '/', str(chuj), ".json"]))
                    shutil.copy(''.join([folder_selected, fb, i, '/', str(chuj), ".json"]), "data")
                    chuj+=1
