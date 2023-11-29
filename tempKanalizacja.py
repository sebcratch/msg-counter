import os
from tkinter import filedialog
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numberByDate
import chooseFolder
import shutil

#dialog wybór folderu
#root = Tk()
#root.withdraw()
chooseFolder.autoFind()
folder_selected = "data"#filedialog.askdirectory()

#sortowanie i przypisanie nadawcy
data = list()
for i in os.listdir(folder_selected):
    f = open(folder_selected+"/"+i, "r")
    a=f.read().split('"is_geoblocked_for_viewer"')[1:-1]
    f.close()

    for i in a:
        pppp = i.split(',')
        data.append((pppp[1][29:-1], pppp[2][23::]))

shutil.rmtree("data")
data = sorted(data, key=lambda x: int(x[1]))


x, y, interv = numberByDate.NumberByDate(data)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interv))
plt.plot(x,y)
plt.grid()
plt.gcf().autofmt_xdate()
plt.show()