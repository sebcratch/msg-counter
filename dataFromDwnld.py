import os
from tkinter import filedialog
from tkinter import *
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



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
    for subFolder in os.listdir(mainfolder):
        importedData = partDataFromDwnld(mainfolder + '/' + subFolder)
        finalList.extend(importedData)
    for i in range(len(finalList)):
        lTime = time.localtime(finalList[i][1])
        lTime = (lTime[0],lTime[1],lTime[2],lTime[3],lTime[4],lTime[5],lTime[6])
        finalList[i] = list((finalList[i][0], lTime))
    finalList = sorted(finalList, key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4], x[1][5]))

    return simplePlotShow(finalList)




def simplePlotShow(masnyBen):
    for i in range(len(masnyBen)):
        masnyBen[i] = (masnyBen[i][1][2], masnyBen[i][1][1], masnyBen[i][1][0])
    masnySet = sorted(set(masnyBen), key=lambda x: (x[2], x[1], x[0]))
    x,y=[],[]
    for i in masnySet:
        dateEm = "/".join([str(v) for v in i])
        x.append(dateEm)
        y.append(masnyBen.count(i))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.show()
    return x

root = Tk()
root.withdraw()
print(fullDataFromDwnld(filedialog.askdirectory()))
