import os
from tkinter import filedialog
from tkinter import *



def listMsgs(file):
    f = open(file, "r")
    






























def dataFromDwnld(folder):
    #ostatni podfolder dla weryfikacji z czego jest
    men = folder.split("/")[-1]

    if men.find("facebook")+1:

        folder = ''.join([folder, '/your_activity_across_facebook/messages/inbox/'])
        
        #wejście w inbox
        for i in os.listdir(folder):
            #wejście w konwersacje
            for y in os.listdir(''.join([folder, i])):
                if y.endswith(".json"):
                    print(y)

    elif men.find("instagram")+1:
        folder = ''.join([folder, '/messages/inbox/'])

        #wejście w inbox
        for i in os.listdir(folder):
            #wejście w konwersacje
            for y in os.listdir(''.join([folder, i])):
                if y.endswith(".json"):
                    print(y)

root = Tk()
root.withdraw()
dataFromDwnld(filedialog.askdirectory())