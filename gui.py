#-------IMPORTS-------#
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *

from database import Database
from taskmanager import TaskManager
from voice import VoiceAssistant
from time import strftime

import threading
import re
#---------END---------#


#------VARIABLES------#
windowHeight = 600
windowWidth = 700
maxWindowMultiplier = 1.25

taskButtonColour = "yellow"

root = tk.Tk()
db = Database("profile.db") 
tm = TaskManager()
va = VoiceAssistant()

profileIDs = db.fetchIDs()
profiles = []
hourDropOptions = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
minuteDropOptions = [
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
    "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
    "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
    "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
    ]

dueDeadlinesAmount = 0
dueRemindersAmount = 0

# Colour
rootBackgroundColour = "#e5ffde"
borderColour = "#a2ff8a"

# Button Images
createProfileImage = tk.PhotoImage(file="Images/Create Profile Button.png")
updateProfileImage = tk.PhotoImage(file="Images/Change Name Button.png")
deleteProfileImage = tk.PhotoImage(file="Images/Delete Profile Button.png")
setDeadlineImage = tk.PhotoImage(file="Images/Set Deadline Button.png")
setReminderImage = tk.PhotoImage(file="Images/Set Reminder Button.png")
importantImage = tk.PhotoImage(file="Images/Important Button.png")
setImage = tk.PhotoImage(file="Images/Set Button.png")
#---------END---------#


#------FUNCTIONS------#
def profileWindow():
    def createProfile():
        profileName = re.sub('[\W_]+', '', inputCreate.get())
        if len(profileName) > 0:
            db.insertProfile(profileName)
        else:
            messagebox.showinfo("Information", "Enter name to create a profile!")

        refreshProfilesList(db)
        profileCombo.config(values=profiles)
        if len(profiles) == 1:
            profileCombo.current(0)

        profileWindow.destroy()
        refreshTaskList(db)

    def deleteProfile():
        if profileCombo.get() == "":
            messagebox.showinfo("Information", "There are no profiles to delete!")
            profileWindow.destroy()
            return
        profileIndex = profileCombo.current()
        profileIDs = db.fetchIDs()
        profileID = profileIDs[profileIndex]
        db.removeProfile(str(profileID)[2:-3])
        db.removeTasks(str(profileID)[2:-3])

        refreshProfilesList(db)
        if len(profiles) != 0:
            profileCombo.config(values=profiles)
            profileCombo.current(0)
        else:
            profileCombo.config(values=[""])
            profileCombo.current(0)

        profileWindow.destroy()
        refreshTaskList(db)

    def updateProfile():
        if profileCombo.get() == "":
            messagebox.showinfo("Information", "There are no profiles to change!")
            profileWindow.destroy()
            return
        profileName = re.sub('[\W_]+', '', inputUpdate.get())
        if len(profileName) > 0:
            profileIndex = profileCombo.current()
            profileIDs = db.fetchIDs()
            profileID = profileIDs[profileIndex]
            db.updateProfile(profileName, str(profileID)[2:-3])
        else:
            messagebox.showinfo("Information", "Enter name to update a profile!")

        refreshProfilesList(db)
        profileCombo.config(values=profiles)
        if len(profiles) == 1:
            profileCombo.current(0)
        else:
            profileCombo.current(profileIndex)

        profileWindow.destroy()
        refreshTaskList()

    profileWindow = tk.Toplevel()
    profileWindow.minsize(350,150)
    profileWindow.maxsize(350,150)
    profileWindow.title("Profile Details")
    profileWindow.attributes("-alpha", 0.95)
    profileWindow.configure(background=rootBackgroundColour)
    profileWindow.grab_set()

    inputCreateFrame = tk.Frame(profileWindow, bg=borderColour)
    inputCreateFrame.place(relx=0.05, rely=0.125, relwidth=0.4, relheight=0.15)
    inputCreate = tk.Entry(inputCreateFrame, borderwidth=0)
    inputCreate.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.7)

    inputUpdateFrame = tk.Frame(profileWindow, bg=borderColour)
    inputUpdateFrame.place(relx=0.05, rely=0.4, relwidth=0.4, relheight=0.15)
    inputUpdate = tk.Entry(inputUpdateFrame, borderwidth=0)
    inputUpdate.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.7)

    currentProfileFrame = tk.Frame(profileWindow, bg=borderColour)
    currentProfileFrame.place(relx=0.05, rely=0.675, relwidth=0.4, relheight=0.15)
    if profileCombo.get() == "":
        currentProfile = "N/A"
    else:
        currentProfile = profileCombo.get()
    currentProfileLabel = tk.Label(currentProfileFrame, text="Profile: "+currentProfile, bg="white")
    currentProfileLabel.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.7)

    createProfileButton = tk.Button(profileWindow, image=createProfileImage, command=createProfile, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    createProfileButton.place(relx=0.55, rely=0.075, relwidth=0.45, relheight=0.25)

    updateProfileButton = tk.Button(profileWindow, image=updateProfileImage, command=updateProfile, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    updateProfileButton.place(relx=0.55, rely=0.35, relwidth=0.45, relheight=0.25)

    deleteProfileButton = tk.Button(profileWindow, image=deleteProfileImage, command=deleteProfile, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    deleteProfileButton.place(relx=0.55, rely=0.625, relwidth=0.45, relheight=0.25)

def addTaskWindow():
    if profileCombo.get() == "":
        messagebox.showinfo("Information", "Create a valid profile first!")
        return

    def addTask():
        profileIndex = profileCombo.current()
        profileIDs = db.fetchIDs()
        profileID = profileIDs[profileIndex]

        if len(input.get()) > 0:
            taskText = input.get()
            allProfileTasks = db.fetchTasks(str(profileID)[2:-3])

            for x in allProfileTasks:
                if taskText == str(x)[2:-3]:
                    addTaskWindow.destroy()
                    messagebox.showinfo("Information", "Task already exists!")
                    return
        else:
            addTaskWindow.destroy()
            messagebox.showinfo("Information", "Enter a task!")
            return

        db.insertTask(str(profileID)[2:-3], taskText)
        refreshTaskList(db)
        addTaskWindow.destroy()

    addTaskWindow = tk.Toplevel()
    addTaskWindow.minsize(350,150)
    addTaskWindow.maxsize(350,150)
    addTaskWindow.title("Add Task")
    addTaskWindow.attributes("-alpha", 0.95)
    addTaskWindow.configure(background=rootBackgroundColour)
    addTaskWindow.grab_set()

    addTaskFrame = tk.Frame(addTaskWindow, bg=borderColour)
    addTaskFrame.place(relx=0.05, rely=0.125, relwidth=0.9, relheight=0.15)
    input = tk.Entry(addTaskFrame, borderwidth=0)
    input.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.7)

    addTaskButton = tk.Button(addTaskWindow, image=addTaskImage, command=addTask, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    addTaskButton.place(relx=0.3, rely=0.35, relwidth=0.4, relheight=0.2)

def removeTask():
    if profileCombo.get() == "":
        return
    taskTextRaw = str(taskList.get("anchor"))
    taskText = taskTextRaw.split(" | DEADLINE:", 1)[0]
    profileIndex = profileCombo.current()
    profileIDs = db.fetchIDs()
    profileID = profileIDs[profileIndex]
    db.removeTask(str(profileID)[2:-3], taskText)
    refreshTaskList(db)

def taskDetailsWindow():
    if taskList.get("anchor") == "":
        messagebox.showinfo("Information", "You do not have a task selected!")
        return

    taskRaw = taskList.get("anchor")
    task = taskRaw.split(" | DEADLINE:", 1)[0]

    taskDetailsWindow = tk.Toplevel()
    taskDetailsWindow.minsize(400,200)
    taskDetailsWindow.maxsize(400,200)
    taskDetailsWindow.title("Task Details")
    taskDetailsWindow.attributes("-alpha", 0.95)
    taskDetailsWindow.configure(background=rootBackgroundColour)
    taskDetailsWindow.grab_set()

    deadlineButton = tk.Button(taskDetailsWindow, image=setDeadlineImage, command=lambda:[calendarWindow(task, 1), taskDetailsWindow.destroy()], borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    deadlineButton.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.15)

    reminderButton = tk.Button(taskDetailsWindow, image=setReminderImage, command=lambda:[calendarWindow(task, 2), taskDetailsWindow.destroy()], borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    reminderButton.place(relx=0.3, rely=0.275, relwidth=0.4, relheight=0.15)

    profileIndex = profileCombo.current()
    profileIDs = db.fetchIDs()
    profileID = profileIDs[profileIndex]

    importantActive = IntVar()
    importantActive.set(db.getIfTaskImportant(str(profileID)[2:-3], task))
    setImportantCheck = tk.Checkbutton(taskDetailsWindow, image=importantImage, variable=importantActive, command=lambda:setDetail(task,4,importantActive.get()), borderwidth=0, bg="#15d798", activebackground="#15d798")
    setImportantCheck.place(relx=0.3, rely=0.625, relwidth=0.4, relheight=0.25)

def calendarWindow(whichTask, whichDetail):
    calendarWindow = tk.Toplevel()
    calendarWindow.minsize(400,400)
    calendarWindow.maxsize(400,400)
    calendarWindow.title("Calendar")
    calendarWindow.attributes("-alpha", 0.95)
    calendarWindow.configure(background=rootBackgroundColour)
    calendarWindow.grab_set()

    today = tm.getTodaysDate()
    cal = Calendar(calendarWindow, selectmode="day", year=today.year, month=today.month, day=today.day)
    cal.place(relwidth=1, relheight=0.75)

    hourDrop = ttk.Combobox(calendarWindow, state="readonly", value=hourDropOptions)
    hourDrop.current(11)
    hourDrop.place(relx=0.350, rely=0.775, relwidth=0.15, relheight=0.05)

    minuteDrop = ttk.Combobox(calendarWindow, state="readonly", value=minuteDropOptions)
    minuteDrop.current(0)
    minuteDrop.place(relx=0.500, rely=0.775, relwidth=0.15, relheight=0.05)

    radioCheckPM = tk.Radiobutton(calendarWindow, text="PM", variable=radioMeridian, value=1, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    radioCheckPM.place(relx=0.350, rely=0.83, relwidth=0.15, relheight=0.05)
    radioCheckAM = tk.Radiobutton(calendarWindow, text="AM", variable=radioMeridian, value=2, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    radioCheckAM.place(relx=0.500, rely=0.83, relwidth=0.15, relheight=0.05)

    setDetailButton = tk.Button(calendarWindow, image=setImage, command=lambda:[setDetail(whichTask,whichDetail,cal.get_date()+" "+str(hourDrop.get())+":"+str(minuteDrop.get())+" "+("PM" if str(radioMeridian.get()) == "1" else "AM")), calendarWindow.destroy()], borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    setDetailButton.place(relx=0.325, rely=0.8875, relwidth=0.35, relheight=0.075)

def setDetail(whichTask, whichDetail, inputDetail):
    profileIndex = profileCombo.current()
    profileIDs = db.fetchIDs()
    profileID = profileIDs[profileIndex]

    db.setTaskDetail(str(profileID)[2:-3], whichTask, whichDetail, inputDetail)

    refreshTaskList(db)

def selectedCombo(event):
    refreshTaskList(db)

def refreshTaskList(currentDatabase):
    if profileCombo.get() == "":
        taskList.delete(0,"end")
        return
    taskList.delete(0,"end")
    profileIndex = profileCombo.current()
    profileIDs = currentDatabase.fetchIDs()
    profileID = profileIDs[profileIndex]

    dbTaskList = currentDatabase.fetchTasks(str(profileID)[2:-3])
    for item in dbTaskList:
        if str(currentDatabase.getDeadline(str(profileID)[2:-3], str(item)[2:-3]))[2:-3] == "0":
            taskList.insert("end", str(item)[2:-3] + " | DEADLINE: " + "N/A")
        else:
            taskList.insert("end", str(item)[2:-3] + " | DEADLINE: " + str(currentDatabase.getDeadline(str(profileID)[2:-3], str(item)[2:-3]))[2:-3])

def refreshProfilesList(currentDatabase):
    profiles.clear()
    profileIDs = currentDatabase.fetchIDs()
    if len(profileIDs) > 0:
        for x in profileIDs:
            profiles.append(currentDatabase.fetchProfileById(str(x)[2:-3]))

def repeatDueDeadlinesCall():
    global dueDeadlinesAmount

    print(tm.getAllDueDeadlines())

    if tm.getAmountOfDueDeadlines() > dueDeadlinesAmount:
        dueDeadlinesWindow()
        dueDeadlinesAmount = tm.getAmountOfDueDeadlines()
    else:
        dueDeadlinesAmount = tm.getAmountOfDueDeadlines()

    root.after(1000, repeatDueDeadlinesCall)

def repeatDueRemindersCall():
    global dueRemindersAmount

    storeAllDueReminders = tm.getAllDueReminders()
    print(storeAllDueReminders)

    if tm.getAmountOfDueReminders() > dueRemindersAmount:
        for x in range(int(tm.getAmountOfDueReminders()*3))[::3]:
            response = messagebox.showinfo("Reminder!", storeAllDueReminders[x+1])
            db.setTaskDetail(storeAllDueReminders[x+2], storeAllDueReminders[x+1], 2, 0)

        dueRemindersAmount = tm.getAmountOfDueReminders()
    else:
        dueRemindersAmount = tm.getAmountOfDueReminders()

    root.after(1000, repeatDueRemindersCall)

def dueDeadlinesWindow():
    deadlinesWindow = tk.Toplevel()
    deadlinesWindow.minsize(650,300)
    deadlinesWindow.maxsize(800,400)
    deadlinesWindow.title("Due Deadlines!")
    deadlinesWindow.grab_set()

    deadlinesList = tk.Listbox(deadlinesWindow)
    deadlinesList.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    storeAllDueDeadlines = tm.getAllDueDeadlines()

    n = 1
    while n < len(storeAllDueDeadlines):

        profileName = str(db.fetchProfileById(storeAllDueDeadlines[n+1]))[2:-3]
        taskDeadline = storeAllDueDeadlines[n-1]
        currentTask = storeAllDueDeadlines[n]

        taskImportance = str(db.getIfTaskImportant(storeAllDueDeadlines[n+1], currentTask))[1:-2]

        if taskImportance == "1":
            deadlinesList.insert("end", " --IMPORTANT--" + " PROFILE: " + profileName + ", TASK: " + currentTask + ", DEADLINE: " + str(taskDeadline.strftime('%d-%m-%Y, %I:%M%p')))
        else:
            deadlinesList.insert("end", "PROFILE: " + profileName + ", TASK: " + currentTask + ", DEADLINE: " + str(taskDeadline.strftime('%d-%m-%Y, %I:%M%p')))
        
        n += 3

def voiceAssistant():
    dbVA = Database("profile.db")
    userCommand = va.interactWithUser()
    
    allProfileNames = dbVA.fetchProfileNames()

    for name in allProfileNames:
        if str(name)[2:-3] == userCommand[0]:
            IDs = dbVA.fetchIDByName(str(name)[2:-3])

            if userCommand[2] == "add task":
                for id in IDs:
                    dbVA.insertTask(str(id)[2:-3], userCommand[1])
            elif userCommand[2] == "remove task":
                for id in IDs:
                    dbVA.removeTask(str(id)[2:-3], userCommand[1])
            elif userCommand[2] == "remove profile":
                for id in IDs:
                    dbVA.removeProfile(str(id)[2:-3])
            elif userCommand[2] == "set deadline":
                for id in IDs:
                    year = userCommand[3]
                    month = userCommand[4]
                    day = userCommand[5]

                    dbVA.setTaskDetail(str(id)[2:-3], userCommand[1], 1, correctDateFormat(day, month, year))
            elif userCommand[2] == "set reminder":
                for id in IDs:
                    year = userCommand[3]
                    month = userCommand[4]
                    day = userCommand[5]

                    dbVA.setTaskDetail(str(id)[2:-3], userCommand[1], 2, correctDateFormat(day, month, year))
            elif userCommand[2] == "set important task":
                for id in IDs:
                    dbVA.setTaskDetail(str(id)[2:-3], userCommand[1], 4, 1)

    if userCommand[2] == "add profile":
        dbVA.insertProfile(re.sub('[\W_]+', '', userCommand[0]))


    # Refresh
    refreshProfilesList(dbVA)
    profileCombo.config(values=profiles)
    if len(profiles) == 0:
        profileCombo.config(values=[""])
        profileCombo.current(0)
    elif len(profiles) == 1:
        profileCombo.current(0)
        
    refreshTaskList(dbVA)

def correctDateFormat(day, month, year):
    if day == "one" or day == "1st" or day == "first" or day == "1":
        formattedDay = "01"
    elif day == "two" or day == "2nd" or day == "second" or day == "2":
        formattedDay = "02"
    elif day == "three" or day == "3rd" or day == "third" or day == "3":
        formattedDay = "03"
    elif day == "four" or day == "4th" or day == "fourth" or day == "4":
        formattedDay = "04"
    elif day == "five" or day == "5th" or day == "fifth" or day == "5":
        formattedDay = "05"
    elif day == "six" or day == "6th" or day == "sixth" or day == "6":
        formattedDay = "06"
    elif day == "seven" or day == "7th" or day == "seventh" or day == "7":
        formattedDay = "07"
    elif day == "eight" or day == "8th" or day == "eighth" or day == "8":
        formattedDay = "08"
    elif day == "nine" or day == "9th" or day == "ninth" or day == "9":
        formattedDay = "09"
    elif day == "ten" or day == "10th" or day == "tenth" or day == "10":
        formattedDay = "10"
    elif day == "eleven" or day == "11th" or day == "eleventh" or day == "11":
        formattedDay = "11"
    elif day == "twelve" or day == "12th" or day == "twelfth" or day == "12":
        formattedDay = "12"
    elif day == "thirteen" or day == "13th" or day == "thirteenth" or day == "13":
        formattedDay = "13"
    elif day == "fourteen" or day == "14th" or day == "fourteenth" or day == "14":
        formattedDay = "14"
    elif day == "fifteen" or day == "15th" or day == "fifteenth" or day == "15":
        formattedDay = "15"
    elif day == "sixteen" or day == "16th" or day == "sixteenth" or day == "16":
        formattedDay = "16"
    elif day == "seventeen" or day == "17th" or day == "seventeenth" or day == "17":
        formattedDay = "17"
    elif day == "eighteen" or day == "18th" or day == "eighteenth" or day == "18":
        formattedDay = "18"
    elif day == "nineteen" or day == "19th" or day == "nineteenth" or day == "19":
        formattedDay = "19"
    elif day == "twenty" or day == "20th" or day == "twentieth" or day == "20":
        formattedDay = "20"
    elif day == "twenty one" or day == "21st" or day == "twenty first" or day == "21":
        formattedDay = "21"
    elif day == "twenty two" or day == "22nd" or day == "twenty second" or day == "22":
        formattedDay = "22"
    elif day == "twenty three" or day == "23rd" or day == "twenty third" or day == "23":
        formattedDay = "23"
    elif day == "twenty four" or day == "24th" or day == "twenty fourth" or day == "24":
        formattedDay = "24"
    elif day == "twenty five" or day == "25th" or day == "twenty fifth" or day == "25":
        formattedDay = "25"
    elif day == "twenty six" or day == "26th" or day == "twenty sixth" or day == "26":
        formattedDay = "26"
    elif day == "twenty seven" or day == "27th" or day == "twenty seventh" or day == "27":
        formattedDay = "27"
    elif day == "twenty eight" or day == "28th" or day == "twenty eighth" or day == "28":
        formattedDay = "28"
    elif day == "twenty nine" or day == "29th" or day == "twenty ninth" or day == "29":
        formattedDay = "29"
    elif day == "thirty" or day == "30th" or day == "thirtieth" or day == "30":
        formattedDay = "30"
    elif day == "thirty one" or day == "31st" or day == "thirty first" or day == "31":
        formattedDay = "31"
    else:
        formattedDay = "01"

    if month == "January":
        formattedMonth = "01"
    elif month == "February":
        formattedMonth = "02"
    elif month == "March":
        formattedMonth = "03"
    elif month == "April":
        formattedMonth = "04"
    elif month == "May":
        formattedMonth = "05"
    elif month == "June":
        formattedMonth = "06"
    elif month == "July":
        formattedMonth = "07"
    elif month == "August":
        formattedMonth = "08"
    elif month == "September":
        formattedMonth = "09"
    elif month == "October":
        formattedMonth = "10"
    elif month == "November":
        formattedMonth = "11"
    elif month == "December":
        formattedMonth = "12"
    else:
        formattedMonth = "01"

    formattedYear = re.sub('[\W_]+', '', year)

    return formattedDay + "/" + formattedMonth + "/" + formattedYear + " 12:00 PM"  
#---------END---------#


#------SETTINGS------#
root.minsize(windowHeight, windowWidth)
root.maxsize(int(windowHeight*maxWindowMultiplier), int(windowWidth*maxWindowMultiplier))
root.title("Family Organiser")
root.iconphoto(True, tk.PhotoImage(file="Images/Icon.png"))
root.geometry(str(windowHeight)+"x"+str(windowWidth))
root.configure(background=rootBackgroundColour)

radioMeridian = tk.IntVar(value="1")
#---------END---------#


#-----COMPONENTS-----#
# User profile section
userFrame = tk.Frame(root, bg=borderColour)
userFrame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.05)

# Combobox
if len(profileIDs) != 0:
    refreshProfilesList(db)
    profileCombo = ttk.Combobox(userFrame, state="readonly", value=profiles)
    profileCombo.current(0)
else:
    profileCombo = ttk.Combobox(userFrame, state="readonly", value=[""])
    profileCombo.current(0)

profileCombo.place(relx=0.005, rely=0.05, relwidth=0.99, relheight=0.9)
profileCombo.bind("<<ComboboxSelected>>", selectedCombo)

# Task view section
taskFrame = tk.Frame(root, bg=borderColour)
taskFrame.place(relx=0.05, rely=0.125, relwidth=0.9, relheight=0.825)

# Listbox for tasks
taskList = tk.Listbox(taskFrame, borderwidth=0)
taskList.place(relx=0.005, rely=0.055, relwidth=0.99, relheight=0.94)
refreshTaskList(db)

# Scrollbar for task list
scrollbar = tk.Scrollbar(taskList)
scrollbar.place(relx=0.975, rely=0, relwidth=0.025, relheight=1)
taskList.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=taskList.yview)

# Button: Add task
addTaskImage = tk.PhotoImage(file="Images/Add Task Button.png")
addTaskButton = tk.Button(taskFrame, image=addTaskImage, command=addTaskWindow, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
addTaskButton.place(relx=0, rely=0, relwidth=0.25, relheight=0.05)

# Button: Remove task
removeTaskImage = tk.PhotoImage(file="Images/Remove Task Button.png")
removeTaskButton = tk.Button(taskFrame, image=removeTaskImage, command=removeTask, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
removeTaskButton.place(relx=0.25, rely=0, relwidth=0.25, relheight=0.05)

# Button: Task details
taskDetailsImage = tk.PhotoImage(file="Images/Task Details Button.png")
taskDetailsButton = tk.Button(taskFrame, image=taskDetailsImage, command=taskDetailsWindow, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
taskDetailsButton.place(relx=0.50, rely=0, relwidth=0.25, relheight=0.05)

# Button: Profile Details
profileDetailsImage = tk.PhotoImage(file="Images/Profile Details Button.png")
profileDetailsButton = tk.Button(taskFrame, image=profileDetailsImage, command=profileWindow, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
profileDetailsButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.05)
#---------END---------#

repeatDueDeadlinesCall()
repeatDueRemindersCall()

threading.Thread(target=voiceAssistant).start()

tk.mainloop()