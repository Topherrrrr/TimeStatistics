from tkinter import *
from tkcalendar import Calendar
import tkinter as tk
import sqlite3
import win32
from datetime import date
import csv
import subprocess
import pathlib
import time
import sys
import copy
import os
import threading
import babel.numbers
import pathlib
dbDir=f"{pathlib.Path().resolve()}\dist\Starter\ActivityList.db"
print(f"DBDIR: {dbDir}")
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import GlobalStuff
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

def exportData():

    #Runs when the "Create CSV" option is clicked, or enter is typed while in the text field
    def leavemini():

        #Creating a mini window with confirmation a CSV was created
        #Only displays "File created"
        popup2=tk.Tk()
        popup2.wm_title("File created")
        label2=tk.Label(popup2,text="CSV file created")
        label2.pack(side="top",fill="x",pady=10)

        #Run openPath to actually create the CSV
        #False is passed in to prevent the CSV from opening after creation
        openPath(False)

        #Remove current popup window
        popup.destroy()

    #Opens the csv file in windows
    def openPath(autoOpen=True):
        #Making the CSV file

        #Each header column in the CSV
        headers=['Date ' 'Activity ' 'Time_spent_in_seconds']

        #Getting the name of the CSV file
        inputTitle=csvTitle.get("1.0","end-1c")
        fileName=f"{inputTitle}.csv"

        #Writing to the file
        with open(fileName, "w+",newline='') as writeList:
            writer=csv.writer(writeList)
            writer.writerow(headers)
            print(f"StartDate: {startDate.selection_get()} endDate: {endDate.selection_get()}")
            #Fetching data from GlobalStuff. startDate and endDate are selected from the popup calendars
            for i in GlobalStuff.fetchData(startDate.selection_get(), endDate.selection_get(), daysBack=pullDate):
                #Converting i to a list to remove any spaces
                newList=list(i)
                newList[1]=i[1].replace(" ","_")
                newList[1]=newList[1].replace(",","")
                newList=[f"{newList[0]} {newList[1]} {newList[2]}"]
                print(f"NewList: {newList}")
                writer.writerow(newList)

        #If "Create and open CSV" was clicked, it'll open the file after creation
        #Otherwise if "Create CSV" is clicked, it will not open
        if autoOpen==True:
            p=subprocess.Popen(f"{inputTitle}.csv", shell=True)


    #Runs when you hit export
    pullOption=dayList.get()
    pullDate=0
    print(f"PullOption: {pullOption}")

    #Getting the amount of data (as specified by the user). It is passed into pullDate when export is clicked
    if pullOption=="Today":
        pullDate=0
    elif pullOption=="Last 7 days":
        pullDate=7
    elif pullOption=="Last 30 days":
        pullDate=30
    elif pullOption=="All":
        pullDate="All"
    elif pullOption=="Range":
        print(f"StartDate: {startDate.selection_get()}, endDate: {endDate.selection_get()}")


    #Getting all the assets for the popup window
    popup=tk.Tk()
    popup.wm_title("File Created")

    #Making the label to ask the user to enter their file name
    label=tk.Label(popup, text="Enter CSV name")
    label.pack(side="top",fill="x", pady=10)

    #Creating the input field
    csvTitle=tk.Text(popup, height=1,width=52)
    csvTitle.bind('<Return>',leavemini)
    csvTitle.pack()

    #Getting the text from the CSV file
    inputTitle=csvTitle.get("1.0","end-1c")

    #Drawing the exit popup button
    exitPopup=tk.Button(popup, text="Create CSV", command=leavemini)
    exitPopup.pack()

    #Drawing the open csv button
    openFile=tk.Button(popup,text="Create and open CSV",command=openPath)
    openFile.pack()
    popup.mainloop()

#The starter menu, which displays the button for graph menus and the raw data
tabHeight=2
tabWidth=15
# graphTab=tk.Button(root, height=tabHeight, width=tabWidth, text="Graphs", command=lambda:displayGraphMenu())
# graphTab.place(x=0,y=0)

def CheckDropdown(event):

    if dayList.get()=="Range":
        startDate.place(x=0,y=100)
        endDate.place(x=300,y=100)
    #
    else:
        print("forgetting")
        startDate.place_forget()
        endDate.place_forget()

dayList=StringVar(root)
dayList.set("Today")
dayOptions=['Today','Last 7 days','Last 30 days','All','Range']
dayInput=tk.OptionMenu(root, dayList,*dayOptions,command=CheckDropdown)
dayInput.place(x=115,y=0)

dateRange=dayList.get()
print(f"DateRange: {dateRange}")
exportToCSV=tk.Button(root, height=tabHeight, width=tabWidth, text="Export to csv", command=lambda:exportData())
exportToCSV.place(x=0,y=0)
endDate=Calendar(root, selectmode='day',year=date.today().year, month=date.today().month, day=date.today().day)

startDate=Calendar(root, selectmode='day',year=date.today().year, month=date.today().month, day=date.today().day)
endDate=Calendar(root, selectmode='day',year=date.today().year, month=date.today().month, day=date.today().day)



root.mainloop()

