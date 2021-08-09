from tkinter import *
import tkinter as tk
import sqlite3
import win32gui
from datetime import date
import matplotlib.pyplot as plt
import matplotlib
import csv
import subprocess
import pathlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import GlobalStuff


matplotlib.use("TkAgg")
root = tk.Tk()

#Defining window size
root.geometry("800x400")
#Defining window title
root.title(" Application Usage ")


#Connecting to the database
connection=sqlite3.connect('ActivityList.db')
c=connection.cursor()
GlobalStuff.startSQL()

#Adding a list of buttons. Controls what is removed when a button is clicked

#The buttons that show up when you click "Graphs"
graphMenuButtons=[]
#The buttons that show up when you hit Raw Data
rawMenuButtons=[]
#The graphs that show up once you click the type of graph you want
graphDisplay=[]

dateString=date.today()



#Displaying a pie chart from the SQL data
# def displayPieChart():
#     for i in graphDisplay:
#         i.get_tk_widget().destroy()
#         graphDisplay.remove(i)
#     #Fetching SQL data, all entries from today
#     activityList=GlobalStuff.fetchData()
#
#    # print(f"ActivityList: {activityList}")
#     #An array of activity names pulled from the SQL query
#     activityName=[item[1] for item in activityList]
#    # print(f"ActivityNames: {activityName}")
#     #The amount of time spent on each activity
#     activityTime=[stuff[2] for stuff in activityList]
#
#     #Making a graph
#     fig=plt.figure(figsize=(6,6), dpi=100)
#     fig.set_size_inches(6,4)
#     #Specifiying that it's a pie graph
#     plt.pie(activityTime,labels=activityName, autopct='%1.1f%%',shadow=True, startangle=140)
#     plt.axis('equal')
#
#     #Adding the graph to the tkinter widget
#     canvasBar=FigureCanvasTkAgg(fig,master=root)
#     canvasBar.draw()
#     canvasBar.get_tk_widget().place(x=120,y=40)
#
#     #Adding the widget to the display, to be removed if the menu changes
#     graphDisplay.append(canvasBar)

#Runs when the "Graphs" button is clicked
# def displayGraphMenu():
#
#     #Get rid of any data in the raw data tab
#     for i in rawMenuButtons:
#         i.destroy()
#
#     #Makes a button that displays a pie graph when clicked
#     pieButton=tk.Button(root, height=2, width=15, text="Pie Chart", command=lambda:displayPieChart())
#     pieButton.place(x=0,y=45)
#     graphMenuButtons.append(pieButton)
#
#     #Makes a button that displays a line graph when clicked
#     lineButton=tk.Button(root, height=2, width=15, text="Line Chart")
#     lineButton.place(x=0, y=90)
#     graphMenuButtons.append(lineButton)
#
#
#     # f = Figure(figsize=(5,5), dpi=100)
#     # a = f.add_subplot(111)
#     # a.plot([1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,10])
#     #
#     # canvas = FigureCanvasTkAgg(f,master=root)
#     # canvas.draw()
#     # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


#Displays when the "Raw data" button is clicked
def displayRawMenu():

    #Destroy any buttons that were generated by the graph menu
    for i in graphMenuButtons:
        i.destroy()
    #Destroy any graphs
    for i in graphDisplay:
        i.get_tk_widget().destroy()
        graphDisplay.remove(i)

    #Get raw data and format it into something easy to read
    rawActivities=GlobalStuff.fetchData()
    formattedActivities=[]
    for i in rawActivities:

        newActivity=(f"On {rawActivities[rawActivities.index(i)][0]} you spent {rawActivities[rawActivities.index(i)][2]} seconds using {rawActivities[rawActivities.index((i))][1]}")
        formattedActivities.append(newActivity)

    #Add a newline between entries
    formattedActivities="\n".join(formattedActivities)

    #Make a label with the data showing
    rawLabel=Label(root,text=str(formattedActivities))
    rawLabel.place(x=0,y=45)
    rawMenuButtons.append(rawLabel)

def exportData():
    def leavemini():
        popup.destroy()
        print("Destroyed")

    def openPath():
        p=subprocess.Popen(f"{dateString}.csv", shell=True)

    headers=['Date','Activity','Time spent in seconds']
    fileName=f"{str(dateString)}.csv"
    with open(fileName, "w+",newline='') as writeList:
        writer=csv.writer(writeList)
        writer.writerow(headers)
        for i in GlobalStuff.fetchData():
            writer.writerow(i)

    popup=tk.Tk()
    popup.wm_title("File Created")
    label=tk.Label(popup, text="CSV created")
    label.pack(side="top",fill="x", pady=10)
    exitPopup=tk.Button(popup, text="Okay", command=leavemini)
    exitPopup.pack()
    openFile=tk.Button(popup,text="Open CSV",command=openPath)
    openFile.pack()
    popup.mainloop()

#The starter menu, which displays the button for graph menus and the raw data
tabHeight=2
tabWidth=15
# graphTab=tk.Button(root, height=tabHeight, width=tabWidth, text="Graphs", command=lambda:displayGraphMenu())
# graphTab.place(x=0,y=0)

exportToCSV=tk.Button(root, height=tabHeight, width=tabWidth, text="Export to csv", command=lambda:exportData())
exportToCSV.place(x=115,y=0)

rawDataTab=tk.Button(root, height=tabHeight, width=tabWidth, text="Raw Data", command=lambda:displayRawMenu())
rawDataTab.place(x=0,y=0)

root.mainloop()
