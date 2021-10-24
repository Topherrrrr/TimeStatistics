import win32gui
import time
from datetime import date
import datetime
import os.path
from os import path
import threading
import GlobalStuff
import sqlite3




startWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}").encode("ascii","ignore")
dudWindow=startWindow.decode("utf-8")


connection=sqlite3.connect('ActivityList.db')
c=connection.cursor()
GlobalStuff.startSQL()



#A function whose sole purpose is to keep the program running
def mainLoopFunction():
    time.sleep(1)

timer=0
mainLoop=threading.Thread(target=mainLoopFunction)
mainLoop.start()
todaysDate=str(date.today())

#while the program is running
while True:

    #Create an empty list of today's activities
    todaysActivities=[]

    #Get the current window and remove any special characters
    currentWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}").encode("ascii","ignore")
    currentWindow=currentWindow.decode("utf-8")

    #Get all activities from today
    todaysActivities=GlobalStuff.fetchData()
    print(f"Today's Activities: {todaysActivities}")
    #Get the second item in each entry (AKA the name of the activity)
    activities=[item[1] for item in todaysActivities]
    print(f"Current Window: {currentWindow} Activities: {activities}")
    #If the current window isn't already in the table...
    if currentWindow not in activities:
        #Create a new entry
        c.execute("INSERT INTO ActivityTable VALUES (:date, :activity, :time)", {'date': todaysDate, 'activity': currentWindow, 'time': 1})
        connection.commit()

    #If it is in the table...
    elif currentWindow in activities:
        #Get how long the user has spent on it
        timeValue=todaysActivities[activities.index(currentWindow)][2]
        #And increment by 1
        timeValue=timeValue+1
        print(f"Time Value {timeValue}")

        #Commit the newly updated value to the table
        c.execute("""UPDATE ActivityTable SET time = :time WHERE activity = :activity AND date = :date""", {'time': timeValue, 'activity': currentWindow, 'date': todaysDate})
        connection.commit()

    #Increase timer by 1. Not used for anything besides heuristic feedback
    timer=timer+1

    #Sleep for 1 second so the while loop is not constantly running
    time.sleep(1)

