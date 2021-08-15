import sqlite3
from datetime import date
import os
import sys
import win32gui
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
startWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}").encode("ascii","ignore")
dudWindow=startWindow.decode("utf-8")

todaysDate=str(date.today())

connection=sqlite3.connect('ActivityList.db')
c=connection.cursor()

#Fetching total data, datePoint is used to pick the starting date we want to pull data from

def fetchData(datePoint=date.today()):
    #Get today's date, to be used when fetching data from the tables
    dateString=str(datePoint)

    #Get all the activities from today
    c.execute("SELECT * FROM ActivityTable")
    #And fill the list with them
    todaysActivities=c.fetchall()

    return todaysActivities

def startSQL():
    startWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}").encode("ascii","ignore")
    dudWindow=startWindow.decode("utf-8")

    todaysDate=str(date.today())

    connection=sqlite3.connect('ActivityList.db')
    c=connection.cursor()


    #Checking if the table exists, if not createa new one with a first entry
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ActivityTable' ''')
    if c.fetchone()[0]==1:
        print("Table exists")
        connection.commit()
    else:
        print("Table is nonexistent")
        c.execute("""CREATE TABLE ActivityTable (
                    date blob,
                    activity text,
                    time integer
                    )""")
        c.execute("INSERT INTO ActivityTable VALUES (:date, :activity, :time)", {'date': todaysDate, 'activity': dudWindow, 'time': 1})
        connection.commit()
