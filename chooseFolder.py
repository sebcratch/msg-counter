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


    #wybór każdego zipa
    for h in os.listdir(folder_selected):

        #wypakuj baranie
        filen = h
        with ZipFile(folder_selected+'/'+filen, "r") as zip:
            print('Extracting all the files now...') 
            zip.extractall() 
            print('Done!') 



        a = os.listdir("your_activity_across_facebook/messages/inbox")
        for i in a:
            addDir = input(i[:i.index("_")]+" ")
            if addDir == "y":
                for subFile in os.listdir("your_activity_across_facebook/messages/inbox/"+i):
                    if subFile.endswith(".json"):
                        os.rename("your_activity_across_facebook/messages/inbox/"+i+'/'+subFile, "your_activity_across_facebook/messages/inbox/"+i+'/'+str(chuj)+".json")
                        shutil.copy("your_activity_across_facebook/messages/inbox/"+i+'/'+str(chuj)+".json", "data")
                        chuj+=1
    shutil.rmtree("your_activity_across_facebook")
