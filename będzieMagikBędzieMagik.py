import numpy as np
from tkinter import filedialog
from tkinter import *
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from math import ceil
import json
import datetime


def getFileInfo(jsonFile):
    f = open(jsonFile, encoding="utf8")
    data = json.load(f)
    f.close()
    participants = (data['participants'][0], data['participants'][1])
    messages = data['messages']
    return messages, participants



def splitToDetailedList(fileInfo):
    messages, participants = fileInfo[0], fileInfo[1]
    participantMessagesLists = ([], [])
    for i in messages:        
        del i["reactions"]
        del i["media"]
        del i["isUnsent"]
        del i["type"]
        siurek = time.localtime(i['timestamp']//1000)
        i["hour"] = " ".join([str(siurek.tm_sec), str(siurek.tm_min), str(siurek.tm_hour)])
        i["date"] = datetime.datetime(int(siurek.tm_year), int(siurek.tm_mon), int(siurek.tm_mday))
        i["messageLength"] = len(i["text"])
        participantMessagesLists[participants.index(i['senderName'])].append(i)

    del messages
    temp1 = sorted(participantMessagesLists[0], key=lambda d: d['timestamp'])
    temp2 = sorted(participantMessagesLists[1], key=lambda d: d['timestamp'])
    participantMessagesLists = (temp1, temp2)
    return (participantMessagesLists, participants)




def addlabels(x,y,z):
    for i in range(len(x)):
        plt.text(x[i], y[i]/2+z[i], y[i], ha = 'center')
        print(x[i], y[i])
    


def dailyPlot(dtldMsgsAndPartcpnts):

    participantMessagesLists, participants = dtldMsgsAndPartcpnts[0], dtldMsgsAndPartcpnts[1]
    comprsdDictFirst, comprsdDictSecnd = dict(), dict()
    firstPartMsgs, secndPartMsgs = [], []


    for i in participantMessagesLists[0]:
        firstPartMsgs.append(i["date"])
    comprsdDictFirst = (dict.fromkeys(firstPartMsgs))

    for i in comprsdDictFirst:
        comprsdDictFirst[i] = firstPartMsgs.count(i)


    for i in participantMessagesLists[1]:
        secndPartMsgs.append(i["date"])
    comprsdDictSecnd = (dict.fromkeys(secndPartMsgs))

    for i in comprsdDictSecnd:
        comprsdDictSecnd[i] = secndPartMsgs.count(i)




    missing_keys = set(comprsdDictFirst.keys()) - set(comprsdDictSecnd.keys())
    for k in missing_keys:
        comprsdDictSecnd[k] = 0
    
    missing_keys = set(comprsdDictSecnd.keys()) - set(comprsdDictFirst.keys())
    for k in missing_keys:
        comprsdDictFirst[k] = 0

    
    comprsdDictFirst = dict(sorted(comprsdDictFirst.items()))
    comprsdDictSecnd = dict(sorted(comprsdDictSecnd.items()))
    
    x = list(comprsdDictFirst.keys())
    y = list(comprsdDictFirst.values())
    z = list(comprsdDictSecnd.values())
   


    plt.figure(figsize = (10, 5))
    plt.bar(x,y, label=participants[0])
    plt.bar(x,z, bottom=y, label=participants[1])

    
    addlabels(x, y, [0 for i in range(len(y))])
    addlabels(x, z, y)
    



    
    


    plt.legend()
    plt.show()
dailyPlot(splitToDetailedList(getFileInfo(filedialog.askopenfilename())))