import os
from tkinter import filedialog
from tkinter import *
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from math import ceil

def listMsgs(file):
    f = open(file, "r", encoding="raw-unicode-escape")
    allMsgs=f.read().split('"type":')[1:-1] #jakiś chujowy podział
    f.close()
    outputList = []
    for i in allMsgs:
        msgInfo = i.split(',') #rozbicie informacji o msg
        sndrTm =(msgInfo[5][16:-1],msgInfo[-2][20::]) #wziąć tylko godzine i nadawce
        pentak = sndrTm[0]#.encode('latin-1').decode('utf-8') #jakaś chujowa konwersja
        outputList.append((pentak, int(sndrTm[1])/1000))
    return outputList




def partDataFromDwnld(folder):

    #ostatni podfolder dla weryfikacji z czego jest
    men = folder.split("/")[-1]

    msgList = []
    if men.find("facebook")+1:

        folder = ''.join([folder, '/messages/inbox/'])
        #print(folder)
            
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





def intervalCalc(masnySet):    #liczenie interwału w wykresie
    fDay = (int(masnySet[0][0]), int(masnySet[0][1]), int(masnySet[0][2])) #krotka dzień pierwszy
    lDay = (int(masnySet[-1][0]), int(masnySet[-1][1]), int(masnySet[-1][2]))
    fDay = time.mktime(dt.datetime(fDay[2], fDay[1], fDay[0]).timetuple()) #dzień pierwszy epoch
    lDay = time.mktime(dt.datetime(lDay[2], lDay[1], lDay[0]).timetuple())
    return ceil((lDay - fDay)/864000)




#pokazanie wykresu dziennego
def simplePlotShow(masnyBen):
    for i in range(len(masnyBen)):
        masnyBen[i] = (str(masnyBen[i][1][2]), str(masnyBen[i][1][1]), str(masnyBen[i][1][0]))
    masnySet = sorted(set(masnyBen), key=lambda x: (int(x[2]), int(x[1]), int(x[0])))
    x,y=[dt.datetime.strptime('/'.join(d),'%d/%m/%Y').date() for d in masnySet],[]
    for i in masnySet:
        y.append(masnyBen.count(i))

    fig = plt.figure()
    fig.patch.set_facecolor('#111111')
    ax = fig.add_subplot(111)
    ax.tick_params(axis='x', colors='#009999')
    ax.tick_params(axis='y', colors='#009999')
    ax.set_facecolor("#343434")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=intervalCalc(masnyBen)))
    ax.bar(x, y, color="#009999")
    
    fig.autofmt_xdate()
    plt.show()




def weekPlotShow(masnyBen):
    for i in range(len(masnyBen)):
        masnyBen[i] = (str(masnyBen[i][1][2]), str(masnyBen[i][1][1]), str(masnyBen[i][1][0]))
    masnySet = sorted(set(masnyBen), key=lambda x: (int(x[2]), int(x[1]), int(x[0])))
    x, y = [], []
    for i in range(len(masnySet)//7):
        x.append(dt.datetime.strptime('/'.join(masnySet[i]), '%d/%m/%Y').date())
    return x




#główna fukcja
def fullDataFromDwnld(mainfolder):
    finalList = []
    for subFolder in os.listdir(mainfolder):
        importedData = partDataFromDwnld(mainfolder + '/' + subFolder)
        finalList.extend(importedData)
    for i in range(len(finalList)):
        lTime = time.localtime(finalList[i][1])#krotka z datą i badziewiami
        lTime = (lTime[0],lTime[1],lTime[2],lTime[3],lTime[4],lTime[5],lTime[6])#krotka z datą
        finalList[i] = list((finalList[i][0], lTime))
    finalList = sorted(finalList, key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4], x[1][5]))

    return simplePlotShow(finalList)




root = Tk()
root.withdraw()
print(fullDataFromDwnld(filedialog.askdirectory()))
