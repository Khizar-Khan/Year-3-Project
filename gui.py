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

from PIL import ImageTk, Image
import threading
import re

from datetime import datetime
#---------END---------#


#------VARIABLES------#
voiceAssistantActive = 0

windowHeight = 600
windowWidth = 700
maxWindowMultiplier = 1.25

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
addTaskImage = tk.PhotoImage(file="Images/Add Task Button.png")
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
        refreshTaskList(db)

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
    def setDescription():
        db.setTaskDetail(str(profileID)[2:-3], task, 3, taskDescriptionBox.get(1.0, "end"))
        taskDetailsWindow.destroy()
    
    def getDescription():
        textHolder = db.getTaskDescription(str(profileID)[2:-3], task)
        taskDescriptionBox.insert(1.0, textHolder)

        taskDescriptionBox.delete(1.0,1.2) #Delete {{ In first line
        taskDescriptionBox.delete("end-1c linestart","end") #Delete {{ In last line

    if taskList.get("anchor") == "":
        messagebox.showinfo("Information", "You do not have a task selected!")
        return

    taskRaw = taskList.get("anchor")
    task = taskRaw.split(" | DEADLINE:", 1)[0]

    taskDetailsWindow = tk.Toplevel()
    taskDetailsWindow.minsize(400,250)
    taskDetailsWindow.maxsize(400,250)
    taskDetailsWindow.title("Task Details")
    taskDetailsWindow.attributes("-alpha", 0.95)
    taskDetailsWindow.configure(background=rootBackgroundColour)
    taskDetailsWindow.grab_set()

    # Details Frame
    detailsFrame = tk.Frame(taskDetailsWindow, bg=rootBackgroundColour)
    detailsFrame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.3)

    deadlineButton = tk.Button(detailsFrame, image=setDeadlineImage, command=lambda:[calendarWindow(task, 1), taskDetailsWindow.destroy()], borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    deadlineButton.place(relx=0, rely=0.0, relwidth=0.4, relheight=0.50)

    reminderButton = tk.Button(detailsFrame, image=setReminderImage, command=lambda:[calendarWindow(task, 2), taskDetailsWindow.destroy()], borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour)
    reminderButton.place(relx=0, rely=0.5, relwidth=0.4, relheight=0.50)

    profileIndex = profileCombo.current()
    profileIDs = db.fetchIDs()
    profileID = profileIDs[profileIndex]

    importantActive = IntVar()
    importantActive.set(db.getIfTaskImportant(str(profileID)[2:-3], task))
    setImportantCheck = tk.Checkbutton(detailsFrame, image=importantImage, variable=importantActive, command=lambda:setDetail(task,4,importantActive.get()), borderwidth=0, bg="#15d798", activebackground="#15d798")
    setImportantCheck.place(relx=0.45, rely=0.25, relwidth=0.5, relheight=0.50)

    # Task description frame
    taskDescriptionFrame = tk.Frame(taskDetailsWindow, bg=rootBackgroundColour)
    taskDescriptionFrame.place(relx=0.05, rely=0.375, relwidth=0.9, relheight=0.65)

    # Task description text
    descriptionLabel = tk.Label(taskDescriptionFrame, text='Task Description:', bg=rootBackgroundColour, anchor="w")
    descriptionLabel.place(relx=0, rely=0, relwidth=1, relheight=0.1)

    taskDescriptionBox = Text(taskDescriptionFrame, font=("Calibri"))
    taskDescriptionBox.place(relx=0, rely=0.1, relwidth=1, relheight=0.675)

    setDetailButton = tk.Button(taskDescriptionFrame, image=setImage, borderwidth=0, bg=rootBackgroundColour, activebackground=rootBackgroundColour, command=setDescription)
    setDetailButton.place(relx=0.25, rely=0.775, relwidth=0.5, relheight=0.2)

    getDescription()

def calendarWindow(whichTask, whichDetail):
    calendarWindow = tk.Toplevel()
    calendarWindow.minsize(400,400)
    calendarWindow.maxsize(400,400)
    calendarWindow.title("Calendar")
    calendarWindow.attributes("-alpha", 0.95)
    calendarWindow.configure(background=rootBackgroundColour)
    calendarWindow.grab_set()

    today = tm.getTodaysDate()
    cal = Calendar(calendarWindow, locale="en_UK", selectmode="day", year=today.year, month=today.month, day=today.day)
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

    db = Database("profile.db")

    taskList.delete(0,"end")
    profileIndex = profileCombo.current()
    profileIDs = currentDatabase.fetchIDs()
    profileID = profileIDs[profileIndex]

    dbTaskList = currentDatabase.fetchTasks(str(profileID)[2:-3])

    for item in dbTaskList:
        taskImportance = str(db.getIfTaskImportant(str(profileID)[2:-3], str(item)[2:-3]))[1:-2]

        if str(currentDatabase.getDeadline(str(profileID)[2:-3], str(item)[2:-3]))[2:-3] == "0":
            if taskImportance == "1":
                taskList.insert("end", str(item)[2:-3] + " | DEADLINE: " + "N/A" + " --IMPORTANT--")
            else:
                taskList.insert("end", str(item)[2:-3] + " | DEADLINE: " + "N/A")
        else:
            if taskImportance == "1":
                taskList.insert("end", str(item)[2:-3] + " | DEADLINE: " + str(currentDatabase.getDeadline(str(profileID)[2:-3], str(item)[2:-3]))[2:-3] + " --IMPORTANT--")
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

    tm.getAllDueDeadlines()

    if tm.getAmountOfDueDeadlines() > dueDeadlinesAmount:
        dueDeadlinesWindow()
        va.speak("You have a due deadline.")
        dueDeadlinesAmount = tm.getAmountOfDueDeadlines()
    else:
        dueDeadlinesAmount = tm.getAmountOfDueDeadlines()

    root.after(1000, repeatDueDeadlinesCall)

def repeatDueRemindersCall():
    global dueRemindersAmount

    storeAllDueReminders = tm.getAllDueReminders()

    if tm.getAmountOfDueReminders() > dueRemindersAmount:
        for x in range(int(tm.getAmountOfDueReminders()*3))[::3]:
            va.speak("You have a reminder.")

            taskImportance = str(db.getIfTaskImportant(storeAllDueReminders[x+2], storeAllDueReminders[x+1]))[1:-2]

            if taskImportance == "1":
                response = messagebox.showinfo("Reminder!", "IMPORTANT | " + storeAllDueReminders[x+1])
            else:
                response = messagebox.showinfo("Reminder!", storeAllDueReminders[x+1])

            db.setTaskDetail(storeAllDueReminders[x+2], storeAllDueReminders[x+1], 2, 0)

        dueRemindersAmount = tm.getAmountOfDueReminders()
    else:
        dueRemindersAmount = tm.getAmountOfDueReminders()

    root.after(1000, repeatDueRemindersCall)

def dueDeadlinesWindow():
    deadlinesWindow = tk.Toplevel(bg=rootBackgroundColour)
    deadlinesWindow.minsize(650,300)
    deadlinesWindow.maxsize(800,400)
    deadlinesWindow.attributes("-alpha", 0.95)
    deadlinesWindow.title("Due Deadlines!")
    deadlinesWindow.grab_set()

    deadlinesList = tk.Listbox(deadlinesWindow, borderwidth=0)
    deadlinesList.place(relx=0.025, rely=0.05, relwidth=0.95, relheight=0.9)

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
    
    while True:
        text = va.getAudio()

        if "hey robot" in text or "hi robot" in text:
            va.speak("Hello, what can I do for you?")
            global voiceAssistantActive
            voiceAssistantActive = 1

            while voiceAssistantActive == 1:
                allProfileNames = dbVA.fetchProfileNames()
                userCommand = va.interactWithUser()

                try:
                    for name in allProfileNames:
                        if str(name)[2:-3] == userCommand[0]:
                            IDs = dbVA.fetchIDByName(str(name)[2:-3])
                            if userCommand[2] == "add task":
                                for id in IDs:
                                    dbVA.insertTask(str(id)[2:-3], userCommand[1])
                                    va.speak("Task added")
                            elif userCommand[2] == "remove task":
                                for id in IDs:
                                    dbVA.removeTask(str(id)[2:-3], userCommand[1])
                                    va.speak("Task removed")
                            elif userCommand[2] == "remove profile":
                                for id in IDs:
                                    dbVA.removeProfile(str(id)[2:-3])
                                    va.speak("profile removed")
                            elif userCommand[2] == "set deadline":
                                for id in IDs:
                                    date = userCommand[3]

                                    oldFormattedDate = datetime.now()
                                    formattedDate = datetime.now()

                                    try:
                                        formattedDate = datetime.strptime(date, '%dth of %B %Y')
                                    except:
                                        pass
                                    try:
                                        formattedDate = datetime.strptime(date, '%drd of %B %Y')
                                    except:
                                        pass
                                    try:
                                        formattedDate = datetime.strptime(date, '%dst of %B %Y')
                                    except:
                                        pass
                                    try:
                                        formattedDate = datetime.strptime(date, '%dnd of %B %Y')
                                    except:
                                        pass

                                    if formattedDate == oldFormattedDate:
                                        va.speak("I'm sorry, I could not do that. Please try again.")
                                        break

                                    try:
                                        day = formattedDate.day
                                        month = formattedDate.month
                                        year = formattedDate.year

                                        dbVA.setTaskDetail(str(id)[2:-3], userCommand[1], 1, correctDateFormat(day, month, year))
                                        va.speak("Deadline is set")
                                    except:
                                        va.speak("I'm sorry, I could not do that. Please try again.")
                            elif userCommand[2] == "set reminder":
                                for id in IDs:
                                    date = userCommand[3]

                                    oldFormattedDate = datetime.now()
                                    formattedDate = datetime.now()

                                    try:
                                        formattedDate = datetime.strptime(date, '%dth of %B %Y')
                                    except:
                                        pass
                                    try:
                                        formattedDate = datetime.strptime(date, '%drd of %B %Y')
                                    except:
                                        pass
                                    try:
                                        formattedDate = datetime.strptime(date, '%dst of %B %Y')
                                    except:
                                        pass
                                    try:
                                        formattedDate = datetime.strptime(date, '%dnd of %B %Y')
                                    except:
                                        pass

                                    if formattedDate == oldFormattedDate:
                                        va.speak("I'm sorry, I could not do that. Please try again.")
                                        break

                                    try:
                                        day = formattedDate.day
                                        month = formattedDate.month
                                        year = formattedDate.year

                                        dbVA.setTaskDetail(str(id)[2:-3], userCommand[1], 2, correctDateFormat(day, month, year))
                                        va.speak("Reminder is set")
                                    except:
                                        va.speak("I'm sorry, I could not do that. Please try again.")
                            elif userCommand[2] == "set important task":
                                for id in IDs:
                                    dbVA.setTaskDetail(str(id)[2:-3], userCommand[1], 4, 1)
                                    va.speak("Task is set as important")
                            elif userCommand[2] == "what tasks":
                                for id in IDs:
                                    allProfileTasksList = dbVA.fetchTasks(str(id)[2:-3])
                                    va.speak("These are the following tasks that you currently have")
                                    taskNum = 0

                                    for task in allProfileTasksList:
                                        taskNum+=1
                                        va.speak("Task " + str(taskNum) + ", " + str(task)[2:-3])

                    if userCommand[2] == "add profile":
                        dbVA.insertProfile(re.sub('[\W_]+', '', userCommand[0]))
                        va.speak("Profile added")

                    if userCommand[2] == "exit":
                        voiceAssistantActive = 0
                except:
                    pass

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
    return str(day) + "/" + str(month) + "/" + str(year) + " 12:00 PM"  
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
# Welcome section
welcomeFrame = tk.Frame(root, bg=rootBackgroundColour)
welcomeFrame.place(relx=0.05, rely=0.005, relwidth=0.9, relheight=0.055)

# Welcome logo
image = Image.open("Images/Logo.png")
image = image.resize((34,38), Image.ANTIALIAS)
welcomeRobotIMG = ImageTk.PhotoImage(image)
canvas = Canvas(welcomeFrame, bg=rootBackgroundColour, bd=0, width=40, height=40, highlightthickness=0)
canvas.create_image(17,19,image=welcomeRobotIMG)
canvas.place(relx=0, rely=0, relwidth=0.25, relheight=1)

# Welcome text
welcomeLabel = tk.Label(welcomeFrame, text='Welcome! Say "Hey Robot" to activate your voice assistant!', bg=rootBackgroundColour, anchor="w")
welcomeLabel.place(relx=0.075, rely=0, relwidth=1, relheight=1)


# User profile section
userFrame = tk.Frame(root, bg=borderColour)
userFrame.place(relx=0.05, rely=0.0625, relwidth=0.9, relheight=0.05)

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
addTaskButton = tk.Button(taskFrame, text="Add Task", fg="white", command=addTaskWindow, borderwidth=1, bg="#15d798", activebackground=rootBackgroundColour, font="Calibri 13 bold", relief=RIDGE)
addTaskButton.place(relx=0, rely=0, relwidth=0.25, relheight=0.05)

# Button: Remove task
removeTaskButton = tk.Button(taskFrame, text="Remove Task", fg="white", command=removeTask, borderwidth=1, bg="#15d798", activebackground=rootBackgroundColour, font="Calibri 13 bold", relief=RIDGE)
removeTaskButton.place(relx=0.25, rely=0, relwidth=0.25, relheight=0.05)

# Button: Task details
taskDetailsButton = tk.Button(taskFrame, text="Task Details", fg="white", command=taskDetailsWindow, borderwidth=1, bg="#15d798", activebackground=rootBackgroundColour, font="Calibri 13 bold", relief=RIDGE)
taskDetailsButton.place(relx=0.50, rely=0, relwidth=0.25, relheight=0.05)

# Button: Profile Details
profileDetailsButton = tk.Button(taskFrame, text="Profile Details", fg="white", command=profileWindow, borderwidth=1, bg="#15d798", activebackground=rootBackgroundColour, font="Calibri 13 bold", relief=RIDGE)
profileDetailsButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.05)
#---------END---------#

repeatDueDeadlinesCall()
repeatDueRemindersCall()

a = threading.Thread(target=voiceAssistant)
a.setDaemon(True)
a.start()

tk.mainloop()