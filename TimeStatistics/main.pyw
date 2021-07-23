import win32gui
import time
from datetime import date
import datetime
import os.path
from os import path
import threading

#A class that's created each time you focus on another window
class activity(object):
    def __init__(self, focus, counter="00:00:01"):
        self.counter=counter
        self.focus=focus
        self.fullString=f"{focus}::{counter}"

    def changeTime(self):
            #Put the time spent into an array, and extract the total seconds from that array
            splitTime=self.counter.split(":")
            fullTime=(int(splitTime[0])*3600)+(int(splitTime[1])*60)+int(splitTime[2])

            #Add one second to the total time, then calculate the hours, minutes, and seconds
            fullTime=fullTime+1
            seconds = fullTime % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            #Update self.counter and fullstring
            self.counter=f"{hour}:{minutes}:{seconds}"
            self.fullString=f"{self.focus}::{self.counter}"


def mainLoopFunction():
    time.sleep(1)



#A list of activity objects
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
                #Create a new activity based off of the imported values
                Activity=activity(importToActivity[0], importToActivity[1])

                #Append it to the list of all activities currently in the program
                activities.append(Activity)



#Otherwise create a new one
else:
    open(f"{dateString}.txt", 'x')
    print("It doesn't exist")


#If there are no activities, create a filler. Gets buggy without at least one activity in the list, hence this block of code
if not activities:
    Activity=activity("Filler")
    activities.append(Activity)

#Timer to provide heuristic feedback to the user. Not critical to the program
timer=0

#Create a thread whose sole purpose is to keep the program alive
mainLoop=threading.Thread(target=mainLoopFunction)
mainLoop.start()

#While the program is running
while True:
    #Get the window the user is focusing on
    currentWindow=str(f"{win32gui.GetWindowText(win32gui.GetForegroundWindow())}")

    #Using the file from today, read each line. If it's not in current activities, add it and create a new entry
    with open(f"{dateString}.txt", 'r') as readList:
        importList=readList.readlines()
        #A list of "focus" properties from the list of activities. Used to identify which activity is which
        activityTopics=[]

        #For each activity, get the focus and append it to activityTopics[]
        for i in activities:
            activityTopics.append(i.focus)


        #Check if the current window is a part of activityTopics[]. AKA, if there is an activity already created for it
        #If it isn't....
        if currentWindow not in activityTopics:
            print(f"Current Window: {currentWindow}")
            #create a new activity and append it to the activity list
            Activity=activity(currentWindow)
            activities.append(Activity)

            #Sometimes we get an entry in the text file titled "::1". Not sure what it is or how it happens, but this block removes the entry in
            #addition to the filler entry when the .txt file is created
            for fillerActivities in activities:
                print(f"Focus: {fillerActivities.focus}")
                if fillerActivities.focus=="Filler" or fillerActivities.focus==False:
                    activities.remove(fillerActivities)


        #If there is a current activity for an imported item....
        elif currentWindow in activityTopics:
            #Get the index of the activity by referencing the activity topic
            f=activityTopics.index(currentWindow)

            #And use that index to increase the amount of time spent on it by 1 second
            activities[f].changeTime()

        #Then write all the activities back
        with open(f"{dateString}.txt",'w') as writeList:
            for i in activities:
                writeList.write(f"{i.fullString}\n")



    timer=timer+1
    print(f"Timer: {timer}")
    time.sleep(1)

