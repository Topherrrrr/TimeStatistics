import win32gui
import time
from datetime import date
import datetime
import os.path
from os import path
import threading

class activity(object):
    def __init__(self, focus, counter=1):
        self.counter=counter
        self.focus=focus
        self.fullString=f"{focus}::{counter}"


def mainLoopFunction():
    time.sleep(1)




activities=[]

#Getting the current date, used for file naming conventions
dateString=str(date.today())
print(f"{dateString}")

#If a file already exists for today, use that file to import prior activities
if path.exists(f"{dateString}.txt"):
    with open(f"{dateString}.txt", 'r') as fillList:
        for i in fillList.readlines():
            if i != '\n':
                importToActivity=i.split("::")
                Activity=activity(importToActivity[0], importToActivity[1])
                activities.append(Activity)



#Otherwise create a new one
else:
    open(f"{dateString}.txt", 'x')
    print("It doesn't exist")

if not activities:
    Activity=activity("Filler")
    activities.append(Activity)

timer=0
mainLoop=threading.Thread(target=mainLoopFunction)
mainLoop.start()
while True:
    currentWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}")

    #Using the file from today, read each line. If it's not in current activities, add it and create a new entry
    with open(f"{dateString}.txt", 'r') as readList:
        importList=readList.readlines()
        activityTopics=[]
        for i in activities:
            activityTopics.append(i.focus)
        #   print(f"Activity topics: {activityTopics}")
        filteredImports=[]
        for i in importList:
            splitImport=i.strip('\n')
            splitImport=splitImport.split("::")
            filteredImports.append(splitImport)



        if currentWindow not in activityTopics:
            print(f"Current Window: {currentWindow}")
            Activity=activity(currentWindow)
            activities.append(Activity)
            for fillerActivities in activities:
                print(f"Focus: {fillerActivities.focus}")
                if fillerActivities.focus=="Filler" or fillerActivities.focus==False:
                    activities.remove(fillerActivities)
        #     print(f"Activity not found. Appending, list now looks like\n{activities}")



        elif currentWindow in activityTopics:
            f=activityTopics.index(currentWindow)
            activities[f].counter=int(activities[f].counter)+1
            activities[f].fullString=f"{activities[f].focus}::{activities[f].counter}"
        #   print(f"Activity found, modifying fullString. It now looks like\n{activities[f].fullString}")


        with open(f"{dateString}.txt",'w') as writeList:
            #    print("Writing")
            for i in activities:
                writeList.write(f"{i.fullString}\n")



    timer=timer+1
    print(f"Timer: {timer}")
    #  print(f"Current activities: {currentActivities[0]}")
    #print(f"Current Window: {win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
    #  for i in currentActivities:
    time.sleep(1)

