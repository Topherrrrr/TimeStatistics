import sqlite3
import datetime as DT
import os
import sys
import win32gui
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
startWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}").encode("ascii","ignore")
dudWindow=startWindow.decode("utf-8")

todaysDate=str(DT.date.today())

connection=sqlite3.connect('ActivityList.db')
c=connection.cursor()

#Fetching total data, datePoint is used to pick the starting date we want to pull data from
#DaysBack is how many days ago we want to pull data from. For example, 7 will pull all data from the last 7 days

def fetchData(date1=None, date2=None, daysBack=0):
    #Get today's date, to be used when fetching data from the tables
    todaysActivities=[]
    if daysBack=="All":
        c.execute(f"SELECT * FROM ActivityTable")
        todaysActivities=c.fetchall()
    elif date1 and date2:
        c.execute(f"SELECT * FROM ActivityTable WHERE date >= :date1 AND date <= :date2",{'date1':date1,'date2':date2})
        todaysActivities=c.fetchall()
        print("Date1 / 2")
    else:
        try:
            today=DT.date.today()
            pullDate=today-DT.timedelta(daysBack)
            c.execute(f"SELECT * FROM ActivityTable WHERE date >= :date",{'date':pullDate})
            print(f"PullDate: {pullDate}")
            todaysActivities=c.fetchall()
        except:
            pass
        finally:
            print(f"DaysBack: {daysBack}")
    return todaysActivities

def startSQL():
    startWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}").encode("ascii","ignore")
    dudWindow=startWindow.decode("utf-8")

    todaysDate=str(DT.date.today())

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
