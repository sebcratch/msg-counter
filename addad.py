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



def count_messages_and_media(participantMessages):
    text_messages = []
    media_messages = []

    for message in participantMessages:
        if message['type'] == "text":
            text_messages.append(message["date"])
        else:
            media_messages.append(message["date"])

    text_count = {date: text_messages.count(date) for date in text_messages}
    media_count = {date: media_messages.count(date) for date in media_messages}

    return text_count, media_count



def initialize_missing_dates(analyzed_span, text_count, media_count):
    for day in datetime_range(analyzed_span):
        if day not in text_count:
            text_count[day] = 0
        if day not in media_count:
            media_count[day] = 0
    
    return dict(sorted(text_count.items())), dict(sorted(media_count.items()))




def plot_data(x_axis, y_st_axis_text, y_st_axis_media, y_nd_axis_text, y_nd_axis_media, participants):
    fig = plt.figure()
    fig.patch.set_facecolor("#181818")
    ax = fig.add_subplot(111)
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    
    ax.tick_params(axis='x', colors='#ffffff')
    ax.tick_params(axis='y', colors='#ffffff')
    ax.set_facecolor("#1F1F1F")
    plt.setp(ax.spines.values(), color="#2B2B2B")

    def addlabels(x, y, z):
        for i in range(len(x)):
            plt.text(x[i], y[i]/2 + z[i], y[i], ha='center')

    y = [sum(x) for x in zip(y_st_axis_text, y_st_axis_media)]
    b = [sum(x) for x in zip(y, y_nd_axis_text)]

    ax.bar(x_axis, y_st_axis_text, label=participants[0], color='#58aff4', edgecolor="white")
    ax.bar(x_axis, y_st_axis_media, bottom=y_st_axis_text, edgecolor="white", color="#2898f1")
    ax.bar(x_axis, y_nd_axis_text, bottom=y, label=participants[1], color='#f49C58', edgecolor="white")
    ax.bar(x_axis, y_nd_axis_media, bottom=b, color="#45763a")

    addlabels(x_axis, y, [0 for _ in range(len(y))])
    addlabels(x_axis, y_nd_axis_text, y)

    ax.legend()
    plt.show()




def dailyPlot(dtldMsgsAndPartcpnts):
    participantMessagesLists, participants, analyzed_span = dtldMsgsAndPartcpnts

    # Process first participant
    text_count_first, media_count_first = count_messages_and_media(participantMessagesLists[0])
    text_count_first, media_count_first = initialize_missing_dates(analyzed_span, text_count_first, media_count_first)

    # Process second participant
    text_count_second, media_count_second = count_messages_and_media(participantMessagesLists[1])
    text_count_second, media_count_second = initialize_missing_dates(analyzed_span, text_count_second, media_count_second)

    # Prepare data for plotting
    x_axis = list(text_count_first.keys())
    y_st_axis_text = list(text_count_first.values())
    y_st_axis_media = list(media_count_first.values())
    y_nd_axis_text = list(text_count_second.values())
    y_nd_axis_media = list(media_count_second.values())

    # Plot the data
    plot_data(x_axis, y_st_axis_text, y_st_axis_media, y_nd_axis_text, y_nd_axis_media, participants)

dailyPlot(load_and_filter_json('C:/Users/S/Downloads/messages/Zuzanna Dębowska_4.json'))