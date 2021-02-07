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

        refreshProfilesList()
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
    profileWindow.grab_set()

    inputCreate = tk.Entry(profileWindow)
    inputCreate.pack()

    inputUpdate = tk.Entry(profileWindow)
    inputUpdate.pack()

    createProfileButton = tk.Button(profileWindow, text="Create Profile", command=createProfile)
    createProfileButton.pack()

    updateProfileButton = tk.Button(profileWindow, text="Change Profile Name", command=updateProfile)
    updateProfileButton.pack()

    deleteProfileButton = tk.Button(profileWindow, text="Delete Profile", command=deleteProfile)
    deleteProfileButton.pack()

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
    addTaskWindow.grab_set()

    input = tk.Entry(addTaskWindow)
    input.pack()

    addTaskButton = tk.Button(addTaskWindow, text="Add Task", command=addTask)
    addTaskButton.pack()

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
    taskDetailsWindow.grab_set()

    deadlineButton = tk.Button(taskDetailsWindow, text="Set Deadline", command=lambda:[calendarWindow(task, 1), taskDetailsWindow.destroy()])
    deadlineButton.pack()

    reminderButton = tk.Button(taskDetailsWindow, text="Set Reminder", command=lambda:[calendarWindow(task, 2), taskDetailsWindow.destroy()])
    reminderButton.pack()

    profileIndex = profileCombo.current()
    profileIDs = db.fetchIDs()
    profileID = profileIDs[profileIndex]

    recurringActive = IntVar()
    recurringActive.set(db.getIfTaskRecurring(str(profileID)[2:-3], task))
    setRecurringCheck = tk.Checkbutton(taskDetailsWindow, text="Set Recurring", variable=recurringActive, command=lambda:setDetail(task,3,recurringActive.get()))
    setRecurringCheck.pack()

    importantActive = IntVar()
    importantActive.set(db.getIfTaskImportant(str(profileID)[2:-3], task))
    setImportantCheck = tk.Checkbutton(taskDetailsWindow, text="Set as Important", variable=importantActive, command=lambda:setDetail(task,4,importantActive.get()))
    setImportantCheck.pack()

def calendarWindow(whichTask, whichDetail):
    calendarWindow = tk.Toplevel()
    calendarWindow.minsize(400,400)
    calendarWindow.maxsize(400,400)
    calendarWindow.title("Calendar")
    calendarWindow.grab_set()

    cal = Calendar(calendarWindow, selectmode="day", year=2021, month=1, day=16)
    cal.pack(fill = "both", expand =True)

    hourDrop = ttk.Combobox(calendarWindow, state="readonly", value=hourDropOptions)
    hourDrop.current(11)
    hourDrop.pack()

    minuteDrop = ttk.Combobox(calendarWindow, state="readonly", value=minuteDropOptions)
    minuteDrop.current(0)
    minuteDrop.pack()

    radioCheckPM = tk.Radiobutton(calendarWindow, text="PM", variable=radioMeridian, value=1)
    radioCheckPM.pack()
    radioCheckAM = tk.Radiobutton(calendarWindow, text="AM", variable=radioMeridian, value=2)
    radioCheckAM.pack()

    setDetailButton = tk.Button(calendarWindow, text="Set", command=lambda:[setDetail(whichTask,whichDetail,cal.get_date()+" "+str(hourDrop.get())+":"+str(minuteDrop.get())+" "+("PM" if str(radioMeridian.get()) == "1" else "AM")), calendarWindow.destroy()])
    setDetailButton.pack(pady=20)

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

radioMeridian = tk.IntVar(value="1")
#---------END---------#


#-----COMPONENTS-----#
# User profile section
userFrame = tk.Frame(root, bg="#cce6ff")
userFrame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.05)

# Combobox
if len(profileIDs) != 0:
    refreshProfilesList(db)
    profileCombo = ttk.Combobox(userFrame, state="readonly", value=profiles)
    profileCombo.current(0)
else:
    profileCombo = ttk.Combobox(userFrame, state="readonly", value=[""])
    profileCombo.current(0)

profileCombo.place(relx=0, rely=0, relwidth=1, relheight=1)
profileCombo.bind("<<ComboboxSelected>>", selectedCombo)

# Task view section
taskFrame = tk.Frame(root, bg="#b3d9ff")
taskFrame.place(relx=0.05, rely=0.125, relwidth=0.9, relheight=0.825)

# Listbox for tasks
taskList = tk.Listbox(taskFrame)
taskList.place(relx=0, rely=0.05, relwidth=1, relheight=1)
refreshTaskList(db)

# Scrollbar for task list
scrollbar = tk.Scrollbar(taskList)
scrollbar.place(relx=0.975, rely=0, relwidth=0.025, relheight=0.95)
taskList.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=taskList.yview)

# Button: Add task
addTaskButton = tk.Button(taskFrame, text="Add Task", bg=taskButtonColour, command=addTaskWindow)
addTaskButton.place(relx=0, rely=0, relwidth=0.25, relheight=0.05)

# Button: Remove task
removeTaskButton = tk.Button(taskFrame, text="Remove Task", bg=taskButtonColour, command=removeTask)
removeTaskButton.place(relx=0.25, rely=0, relwidth=0.25, relheight=0.05)

# Button: Task details
taskDetailsButton = tk.Button(taskFrame, text="Task Details", bg=taskButtonColour, command=taskDetailsWindow)
taskDetailsButton.place(relx=0.50, rely=0, relwidth=0.25, relheight=0.05)

# Button: Profile Details
profileDetailsButton = tk.Button(taskFrame, text="Profile Details", bg=taskButtonColour, command=profileWindow)
profileDetailsButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.05)
#---------END---------#

repeatDueDeadlinesCall()
repeatDueRemindersCall()

threading.Thread(target=voiceAssistant).start()

tk.mainloop()