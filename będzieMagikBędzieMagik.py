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


def get_first_and_last_date_of_list(messages):
    messages = sorted(messages, key=lambda x: x["timestamp"])
    return (messages[0]['date'], messages[-1]['date'])
    


def datetime_range(days):
    span = days[1] - days[0]
    for i in range(span.days + 1):
        yield days[0] + datetime.timedelta(days=i)
    




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

    analyzed_span = get_first_and_last_date_of_list(filtered_data)

    return (participants_message_lists, participants, analyzed_span)




def dailyPlot(dtldMsgsAndPartcpnts):

    participantMessagesLists, participants = dtldMsgsAndPartcpnts[0], dtldMsgsAndPartcpnts[1]
    analyzed_span = dtldMsgsAndPartcpnts[2]
    comprsdDictFirst, comprsdDictSecnd = dict(), dict()
    firstPartMsgs, secndPartMsgs = [], []
    firstPartMdia, secndPartMdia = [], []


    for i in participantMessagesLists[0]:
        if i['type'] == "text":
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
        if i['type'] in ["text"]:
            secndPartMsgs.append(i["date"])
        else:
            secndPartMdia.append(i["date"])

    comprsdDictSecnd = (dict.fromkeys(secndPartMsgs))
    mediaDictSecnd = (dict.fromkeys(secndPartMdia))
    for i in comprsdDictSecnd:
        comprsdDictSecnd[i] = secndPartMsgs.count(i)
    for i in mediaDictSecnd:
        mediaDictSecnd[i] = secndPartMdia.count(i)


    for day in list(datetime_range(analyzed_span)):
        if day not in comprsdDictFirst.keys():
            comprsdDictFirst[day]=0
        if day not in comprsdDictSecnd.keys():
            comprsdDictSecnd[day]=0
        if day not in mediaDictFirst.keys():
            mediaDictFirst[day]=0
        if day not in mediaDictSecnd.keys():
            mediaDictSecnd[day]=0
    comprsdDictFirst, comprsdDictSecnd = dict(sorted(comprsdDictFirst.items())), dict(sorted(comprsdDictSecnd.items()))
    mediaDictFirst, mediaDictSecnd = dict(sorted(mediaDictFirst.items())), dict(sorted(mediaDictSecnd.items()))


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
    


    x_axis = list(comprsdDictFirst.keys())
    y_st_axis_text = list(comprsdDictFirst.values())
    y_st_axis_media = list(mediaDictFirst.values())
    y_nd_axis_media = list(mediaDictSecnd.values())
    y_nd_axis_text = list(comprsdDictSecnd.values())   



    y = [sum(x) for x in zip(y_st_axis_text, y_st_axis_media)]
    b = [sum(x) for x in zip(y, y_nd_axis_text)]
    print(y)
    print(y_st_axis_text)

    ax.bar(x_axis,y_st_axis_text, label=participants[0], color='#58aff4', edgecolor="white")
    ax.bar(x_axis, y_st_axis_media, bottom=y_st_axis_text, edgecolor="white", color="#2898f1")
    ax.bar(x_axis,y_nd_axis_text, bottom=y, label=participants[1], color='#f49C58', edgecolor="white")
    ax.bar(x_axis, y_nd_axis_media, bottom=b, color="#45763a")
    
    addlabels(x_axis, y, [0 for i in range(len(y))])
    addlabels(x_axis, y_nd_axis_text, y)
    
    ax.legend()
    plt.show()
dailyPlot(load_and_filter_json('C:/Users/S/Downloads/messages/Zuzanna Dębowska_4.json'))