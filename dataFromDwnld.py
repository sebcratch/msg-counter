import os
from tkinter import filedialog
from tkinter import *



def listMsgs(file):
    f = open(file, "r", encoding="raw-unicode-escape")
    allMsgs=f.read().split('"is_geoblocked_for_viewer"')[1:-1] #jakiś chujowy podział
    f.close()
    outputList = []
    for i in allMsgs:
        msgInfo = i.split(',') #rozbicie wiadomości o msg
        sndrTm =(msgInfo[1][29:-1], msgInfo[2][23::]) #wziąć tylko nadawce i godzine
        pentak = sndrTm[0].encode('latin-1').decode('utf-8') #jakaś chujowa konwersja
        outputList.append((pentak, int(sndrTm[1])/1000))
    return outputList




def partDataFromDwnld(folder):

    #ostatni podfolder dla weryfikacji z czego jest
    men = folder.split("/")[-1]

    msgList = []
    if men.find("facebook")+1:

        folder = ''.join([folder, '/your_activity_across_facebook/messages/inbox/'])
            
        #wejście w inbox
        for i in os.listdir(folder):
            #wejście w konwersacje
            for y in os.listdir(''.join([folder, i])):
                if y.endswith(".json"):
                    msgList.extend(listMsgs(''.join([folder, '/', i, '/', y]))) #dodanie do listy wyjściowej krotki name date


    elif men.find("instagram")+1:

        folder = ''.join([folder, '/messages/inbox/'])

        #wejście w inbox
        for i in os.listdir(folder):
            #wejście w konwersacje
            for y in os.listdir(''.join([folder, i])):
                if y.endswith(".json"):
                    msgList.extend(listMsgs(''.join([folder, '/' ,i, '/', y]))) #dodanie do listy wyjściowej krotki name date

    return msgList




def fullDataFromDwnld(mainfolder):
    finalList = []
    finalSett = set()
    for subFolder in os.listdir(mainfolder):
        importedData = partDataFromDwnld(mainfolder + '/' + subFolder)
        finalList.extend(importedData)
    for i in range(len(set(finalList))):
        print(i)
    return finalSett, finalList

root = Tk()
root.withdraw()
(fullDataFromDwnld(filedialog.askdirectory()))
