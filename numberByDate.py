import time
import datetime as dt
def NumberByDate(data):
    dateList=list()
    dateSet = set()
    dateNumb=list()
    mas = 0
    menos = 9999999999999999999999999
    for i in range(len(data)):
        sEpoch = int(data[i][1])/1000
        mas = max(mas, sEpoch)
        menos = min(menos, sEpoch)
        lTime = time.localtime(sEpoch)
        date = (lTime.tm_mday, lTime.tm_mon, lTime.tm_year)
        dateList.append(date)
    dateSet=sorted(set(dateList), key=lambda x: (x[2], x[1], x[0]))

    for i in range(len(dateSet)):
        dateNumb.append(dateList.count(dateSet[i]))



    plotList=[]
    for i in dateSet:
        sur = '/'.join([str(w) for w in i])
        plotList.append(sur)
    x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in plotList]
    y = dateNumb
    interv = int((mas-menos)//691200)+1
    return x, y, interv
    
    #print(max(dateNumb))