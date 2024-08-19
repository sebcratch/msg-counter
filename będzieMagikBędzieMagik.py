from tkinter import filedialog
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import datetime
import sys

def filter_message(message):
    keys_to_keep = ['senderName', 'text', 'timestamp', 'type']
    return {key: message[key] for key in message.keys() if key in keys_to_keep}


def load_and_filter_json(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        
    filtered_data = [filter_message(message) for message in data['messages']]
    participants = tuple(data['participants'])
    participants_message_lists = [[],[]]

    for message in filtered_data:
        #remove last 3 digits, unneeded
        message_time = time.localtime(message['timestamp']//1000)    
   
        message["hour"] = " ".join([str(message_time.tm_sec), str(message_time.tm_min), str(message_time.tm_hour)])                
        message["date"] = datetime.datetime(int(message_time.tm_year), int(message_time.tm_mon), int(message_time.tm_mday))        
        message["messageLength"] = len(message["text"])                                                                               
        participants_message_lists[participants.index(message['senderName'])].append(message) 
    return (participants_message_lists, participants)




def dailyPlot(dtldMsgsAndPartcpnts):

    participantMessagesLists, participants = dtldMsgsAndPartcpnts[0], dtldMsgsAndPartcpnts[1]
    comprsdDictFirst, comprsdDictSecnd = dict(), dict()
    firstPartMsgs, secndPartMsgs = [], []
    firstPartMdia, secndPartMdia = [], []


    for i in participantMessagesLists[0]:
        if i['type'] in ["text", "placeholder"]:
            firstPartMsgs.append(i["date"])
        else:
            firstPartMdia.append(i["date"])

    comprsdDictFirst = (dict.fromkeys(firstPartMsgs))
    mediaDictFirst = (dict.fromkeys(firstPartMdia))
    for i in comprsdDictFirst:
        comprsdDictFirst[i] = firstPartMsgs.count(i)
    for i in mediaDictFirst:
        mediaDictFirst[i] = firstPartMdia.count(i)


    for i in participantMessagesLists[1]:
        if i['type'] in ["text", "placeholder"]:
            secndPartMsgs.append(i["date"])
        else:
            secndPartMdia.append(i["date"])

    comprsdDictSecnd = (dict.fromkeys(secndPartMsgs))
    mediaDictSecnd = (dict.fromkeys(secndPartMdia))
    for i in comprsdDictSecnd:
        comprsdDictSecnd[i] = secndPartMsgs.count(i)
    for i in mediaDictSecnd:
        mediaDictSecnd[i] = secndPartMdia.count(i)




    missing_keys = set(comprsdDictFirst.keys()) - set(comprsdDictSecnd.keys())
    for k in missing_keys:
        comprsdDictSecnd[k] = 0
    
    missing_keys = set(comprsdDictSecnd.keys()) - set(comprsdDictFirst.keys())
    for k in missing_keys:
        comprsdDictFirst[k] = 0

    missing_keys = set(comprsdDictSecnd.keys()) - set(mediaDictFirst.keys())
    for k in missing_keys:
        mediaDictFirst[k] = 0

    missing_keys = set(comprsdDictSecnd.keys()) - set(mediaDictSecnd.keys())
    for k in missing_keys:
        mediaDictSecnd[k] = 0
    
    missing_keys = set(mediaDictFirst.keys()) - set(comprsdDictFirst.keys())
    for k in missing_keys:
        comprsdDictFirst[k] = 0

    missing_keys = set(mediaDictFirst.keys()) - set(comprsdDictSecnd.keys())
    for k in missing_keys:
        comprsdDictSecnd[k] = 0


    comprsdDictFirst = dict(sorted(comprsdDictFirst.items()))
    comprsdDictSecnd = dict(sorted(comprsdDictSecnd.items()))
    mediaDictFirst = dict(sorted(mediaDictFirst.items()))
    mediaDictSecnd = dict(sorted(mediaDictSecnd.items()))

    fig = plt.figure()
    fig.patch.set_facecolor("#181818")
    ax = fig.add_subplot(111)
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    
    ax.tick_params(axis='x', colors='#ffffff')
    ax.tick_params(axis='y', colors='#ffffff')
    ax.set_facecolor("#1F1F1F")
    plt.setp(ax.spines.values(), color="#2B2B2B")

    def addlabels(x,y,z):
        for i in range(len(x)):
            plt.text(x[i], y[i]/2+z[i], y[i], ha = 'center')
    




    x = list(comprsdDictFirst.keys())
    y = list(comprsdDictFirst.values())
    d = list(mediaDictFirst.values())
    l = list(mediaDictSecnd.values())
    z = list(comprsdDictSecnd.values())
    f = [sum(x) for x in zip(y, d)]
    g = [sum(x) for x in zip(z, f)]




    print(z)
    print(f)
    ax.bar(x,y, label=participants[0], color='#58aff4', edgecolor="white")
    ax.bar(x, d, bottom=y, edgecolor="white", color="#2898f1")
    ax.bar(x,z, bottom=f, label=participants[1], color='#f49C58', edgecolor="white")
    ax.bar(x, l, bottom=g, edgecolor="white", color="#f18028")


    
    addlabels(x, y, [0 for i in range(len(y))])
    addlabels(x, z, y)
    


    ax.legend()
    plt.show()
dailyPlot(load_and_filter_json(filedialog.askopenfilename()))