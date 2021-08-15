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

#What runs when you click export data
def exportData():

    #Closing the popup window when "Ok" is clicked
    def leavemini():
        popup.destroy()
        print("Destroyed")

    #Opens the csv file
    def openPath():
        p=subprocess.Popen(f"{dateString}.csv", shell=True)

    #Title for each column
    headers=['Date','Activity','Time spent in seconds']

    #Making the file name the date + .csv
    fileName=f"{str(dateString)}.csv"

    #Writing to the csv file
    with open(fileName, "w+",newline='') as writeList:
        writer=csv.writer(writeList)
        writer.writerow(headers)
        for i in GlobalStuff.fetchData():
            writer.writerow(i)

    #Code for the popup window once the file is created and has data
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

#Exporting the data to a csv file
exportToCSV=tk.Button(root, height=tabHeight, width=tabWidth, text="Export to csv", command=lambda:exportData())
exportToCSV.place(x=115,y=0)

#Adding raw data to the field
rawDataTab=tk.Button(root, height=tabHeight, width=tabWidth, text="Raw Data", command=lambda:displayRawMenu())
rawDataTab.place(x=0,y=0)

root.mainloop()

